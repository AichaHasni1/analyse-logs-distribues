from django.contrib import admin
from django.urls import path
from comptes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
  
    path('deconnexion/', views.deconnexion, name='deconnexion'),  # Utilisez la vue de déconnexion personnalisée
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('telecharger/', views.telecharger_logs, name='telecharger_logs'),
    path('logs/', views.consulter_logs, name='consulter_logs'),


]
