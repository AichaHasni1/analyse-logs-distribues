from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserCreationForm  # type: ignore
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import os

# Vue d'inscription
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

# Vue de connexion
def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

# Redirection vers le dashboard après connexion
from django.urls import reverse
@login_required
def acceuil(request):
    return redirect(reverse('dashboard'))

# Vue de déconnexion
def deconnexion(request):
    logout(request)
    return redirect('connexion')

# Vue du dashboard
@login_required
def dashboard_view(request):
    stats = analyser_logs()
    print(stats)
    return render(request, 'dashboard.html', {'stats': stats})

# Fonction pour analyser les logs
def analyser_logs():
    path = "D:/S8/systeeme repartis/PROJET/analyse-logs-distribues/logs/ssh.log"
    total, failed, accepted, users = 0, 0, 0, set()

    if os.path.exists(path):
        print(f"Le fichier {path} existe.")
    else:
        print(f"Le fichier {path} n'existe pas.")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                total += 1
                if "Failed password" in line:
                    failed += 1
                elif "Accepted" in line:
                    accepted += 1
                if "for" in line:
                    parts = line.split()
                    idx = parts.index("for")
                    if idx + 1 < len(parts):
                        users.add(parts[idx + 1])

        # Affiche les statistiques pour vérifier
        print(f"Total: {total}, Failed: {failed}, Accepted: {accepted}, Users: {len(users)}")
    except Exception as e:
        print(f"Erreur lors de l'analyse des logs : {e}")

    return {
        "total": total,
        "failed": failed,
        "accepted": accepted,
        "users": len(users)
    }
