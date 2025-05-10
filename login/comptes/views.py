import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse
from .form import CustomUserCreationForm  # type: ignore

# ----------------- Vue d'inscription -----------------
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

# ----------------- Vue de connexion -----------------
def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

# ----------------- Vue d'accueil (redirige vers dashboard) -----------------
@login_required
def accueil(request):
    return redirect(reverse('dashboard'))

# ----------------- Vue de déconnexion -----------------
def deconnexion(request):
    logout(request)
    return redirect('connexion')

# ----------------- Vue du dashboard -----------------
@login_required
def dashboard_view(request):
    stats = analyser_logs()
    return render(request, 'dashboard.html', {'stats': stats})

# ----------------- Fonction d'analyse des logs -----------------
from collections import Counter
import os
from datetime import datetime
 

def analyser_logs():
    path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh.log"
    cleaned_path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh_cleaned.log"

    total_logs, failed_logs, accepted_logs, users = 0, 0, 0, []
    hourly_logs = Counter()
    error_counter = Counter()
    logs_per_user = Counter()

    current_year = datetime.now().year

    if not os.path.exists(path):
        print(f"Le fichier {path} n'existe pas.")
        return {}

    valid_lines = []

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_logs += 1
                parts = line.split()
                if len(parts) < 3:
                    continue

                # Construire le timestamp complet avec l'année
                try:
                    date_str = " ".join(parts[:3])  # ex: "Apr 24 15:34:03"
                    full_timestamp = f"{current_year} {date_str}"
                    hour = datetime.strptime(full_timestamp, "%Y %b %d %H:%M:%S")
                except ValueError as e:
                    print(f"Erreur de date dans la ligne supprimée: {line.strip()}, erreur: {e}")
                    continue  # ligne ignorée

                # Si tout est bon, ajouter à la liste des lignes valides
                valid_lines.append(line)
                hourly_logs[hour.hour] += 1

                if "Failed password" in line:
                    failed_logs += 1
                    error_counter["Failed password"] += 1
                elif "Accepted" in line:
                    accepted_logs += 1
                    error_counter["Accepted password"] += 1

                if "for" in line:
                    try:
                        idx = parts.index("for")
                        if idx + 1 < len(parts):
                            user = parts[idx + 1]
                            logs_per_user[user] += 1
                    except ValueError:
                        pass

        # Écrire les lignes valides dans un nouveau fichier nettoyé
        with open(cleaned_path, 'w', encoding='utf-8') as cleaned_file:
            cleaned_file.writelines(valid_lines)

        user_counts = Counter(logs_per_user)
        top_users = user_counts.most_common(5)
        avg_logs_per_user = sum(logs_per_user.values()) / len(logs_per_user) if logs_per_user else 0
        most_frequent_error = error_counter.most_common(1)[0][0] if error_counter else ""
        last_log = valid_lines[-1] if valid_lines else "Aucun log"
        error_rate = (failed_logs / (accepted_logs + failed_logs) * 100) if (accepted_logs + failed_logs) > 0 else 0

        logs_per_hour_list = list(hourly_logs.items())

        return {
            "total": total_logs,
            "failed": failed_logs,
            "accepted": accepted_logs,
            "users": len(set(logs_per_user.keys())),
            "top_users": top_users,
            "logs_per_hour": logs_per_hour_list,
            "avg_logs_per_user": avg_logs_per_user,
            "most_frequent_error": most_frequent_error,
            "last_log": last_log,
            "error_rate": error_rate
        }

    except Exception as e:
        print(f"Erreur lors de l'analyse des logs : {e}")
        return {}

# ----------------- Téléchargement du fichier de logs -----------------
def telecharger_logs(request):
    log_path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh.log"
    if os.path.exists(log_path):
        return FileResponse(open(log_path, 'rb'), as_attachment=True, filename='ssh.log')
    else:
        messages.error(request, "Le fichier de logs est introuvable.")
        return redirect('dashboard')

# ----------------- Consultation du fichier de logs -----------------
def consulter_logs(request):
    log_path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh.log"
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lignes = f.readlines()
    except FileNotFoundError:
        lignes = ["Fichier de logs introuvable."]
    
    return render(request, 'consulter_logs.html', {'logs': lignes})
