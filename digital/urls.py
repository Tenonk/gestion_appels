from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Classes
    path('classes/', views.liste_classes, name='liste_classes'),
    path('classes/creer/', views.creer_classe, name='creer_classe'),
    path('classes/<int:id>/', views.detail_classe, name='detail_classe'),
    
    # Étudiants
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/creer/', views.creer_etudiant, name='creer_etudiant'),
    path('etudiants/<int:id>/', views.detail_etudiant, name='detail_etudiant'),
    path('etudiants/<int:id>/modifier/', views.modifier_etudiant, name='modifier_etudiant'),
    
    # Cours
    path('cours/', views.liste_cours, name='liste_cours'),
    path('cours/creer/', views.creer_cours, name='creer_cours'),
    path('cours/<int:id>/', views.detail_cours, name='detail_cours'),
    
    # Appels
    path('seances/', views.liste_seances, name='liste_seances'),
    path('seances/<int:seance_id>/appel/', views.faire_appel, name='faire_appel'),
]