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

@login_required
def dashboard_view(request):
    stats = analyser_logs()
    
    # Préparation des données pour le template
    context = {
        'stats': {
            'total_logs': stats.get('total_logs', 0),
            'failed_logins': stats.get('failed_logins', 0),
            'accepted_logins': stats.get('accepted_logins', 0),
            'unique_users': stats.get('unique_users', 0),
            'hours': [f"{h:02d}:00" for h in range(24)],  # Format "00:00" à "23:00"
            'hourly_data': stats.get('hourly_data', [0]*24),
            'error_rate': stats.get('error_rate', 0),
            'avg_logs_per_user': stats.get('avg_logs_per_user', 0),
            'most_common_error': stats.get('most_common_error', 'N/A'),
            'last_log': stats.get('last_log', 'Aucun log disponible'),
            'last_update': stats.get('last_update', 'N/A')
        }
    }
    return render(request, 'dashboard.html', context)

from collections import Counter
import os
from datetime import datetime
import re

def analyser_logs():
    """Analyse les logs SSH et retourne des statistiques clés sans l'activité horaire"""
    # Chemins des fichiers
    log_path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh.log"
    cleaned_path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh_cleaned.log"
    
    # Initialisation des compteurs simplifiée
    stats = {
        "total_logs": 0,
        "failed_logins": 0,
        "accepted_logins": 0,
        "unique_users": set(),
        "error_messages": Counter(),
        "logs_per_user": Counter(),
        "most_common_error": "Aucune erreur",
        "last_log": "Aucun log disponible",
        "last_update": datetime.now().strftime("%H:%M:%S"),
        "error_rate": 0.0,
        "avg_logs_per_user": 0.0
    }

    # Vérification de l'existence du fichier
    if not os.path.exists(log_path):
        print(f"Fichier {log_path} introuvable")
        return stats

    # Expressions régulières optimisées
    patterns = {
        "auth": re.compile(r"(?:Failed|Accepted) password for (?:invalid user )?(\S+)"),
        "error": re.compile(r"error: (.+?)(?:\[|$)"),
        "invalid": re.compile(r"Invalid user (\S+)")
    }

    valid_lines = []

    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stats["total_logs"] += 1
                line = line.strip()
                if not line:
                    continue

                # Analyse du contenu
                user = None
                
                if "Failed password" in line:
                    stats["failed_logins"] += 1
                    match = patterns["auth"].search(line) or patterns["invalid"].search(line)
                    if match:
                        user = match.group(1)
                        stats["error_messages"]["Failed password"] += 1
                
                elif "Accepted password" in line:
                    stats["accepted_logins"] += 1
                    match = patterns["auth"].search(line)
                    if match:
                        user = match.group(1)
                
                elif "error:" in line:
                    match = patterns["error"].search(line)
                    if match:
                        stats["error_messages"][match.group(1)] += 1
                
                if user:
                    stats["unique_users"].add(user)
                    stats["logs_per_user"][user] += 1
                
                valid_lines.append(line)

        # Calcul des statistiques finales
        stats["unique_users"] = len(stats["unique_users"])
        
        total_auth = stats["accepted_logins"] + stats["failed_logins"]
        if total_auth > 0:
            stats["error_rate"] = round((stats["failed_logins"] / total_auth * 100), 2)
        
        if stats["unique_users"] > 0:
            stats["avg_logs_per_user"] = round(
                sum(stats["logs_per_user"].values()) / stats["unique_users"], 
                2
            )
        
        if stats["error_messages"]:
            stats["most_common_error"] = stats["error_messages"].most_common(1)[0][0]
        
        if valid_lines:
            stats["last_log"] = valid_lines[-1][:100] + ("..." if len(valid_lines[-1]) > 100 else "")

        # Sauvegarde des logs nettoyés
        with open(cleaned_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(valid_lines))

    except Exception as e:
        print(f"Erreur lors de l'analyse des logs: {e}")
        stats["most_common_error"] = f"Erreur système: {str(e)}"

    return stats
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



import os
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings

def get_ndjson_files(request):
    # Chemin ABSOLU vers le dossier dashboard à la racine
    dashboard_dir = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'dashboard'))
    
    try:
        if not os.path.exists(dashboard_dir):
            return JsonResponse({'error': f'Dossier introuvable: {dashboard_dir}'}, status=404)
            
        files = [
            f for f in os.listdir(dashboard_dir) 
            if f.endswith('.ndjson') and os.path.isfile(os.path.join(dashboard_dir, f))
        ]
        return JsonResponse(files, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

 
from pathlib import Path

import os
from pathlib import Path
 

def download_file(request, filename):
    # Chemin absolu vers le dossier dashboard
    dashboard_dir = Path(settings.BASE_DIR).parent / 'dashboard'
    
    # Protection contre les attaques par chemin
    filename = os.path.basename(filename)
    if not filename.endswith('.ndjson'):
        raise Http404("Seuls les fichiers .ndjson sont autorisés")
    
    file_path = dashboard_dir / filename
    
    if not file_path.exists():
        available_files = [f.name for f in dashboard_dir.glob('*.ndjson')]
        print(f"Fichiers disponibles: {available_files}")  # Debug
        raise Http404(f"Fichier {filename} non trouvé. Fichiers disponibles: {', '.join(available_files)}")
    
    return FileResponse(open(file_path, 'rb'), as_attachment=True)
    
    
def test_files_view(request):
    from django.http import JsonResponse
    dashboard_dir = Path(settings.BASE_DIR).parent / 'dashboard'
    files = {
        'chemin': str(dashboard_dir),
        'fichiers': [f.name for f in dashboard_dir.glob('*')],
        'fichiers_ndjson': [f.name for f in dashboard_dir.glob('*.ndjson')]
    }
    return JsonResponse(files)

def test_download(request):
    from django.http import HttpResponse
    test_file = Path(settings.BASE_DIR).parent / 'dashboard' / 'dash1.ndjson'
    exists = test_file.exists()
    return HttpResponse(f"Test: {test_file} existe? {exists}")