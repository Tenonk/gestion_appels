from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'nombre_etudiants', 'date_creation')
    search_fields = ('nom',)
    list_filter = ('niveau', 'date_creation')

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('numero_matricule', 'nom', 'prenom', 'classe', 'statut', 'email')
    list_filter = ('classe', 'statut', 'date_inscription')
    search_fields = ('numero_matricule', 'nom', 'prenom', 'email')

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'classe', 'enseignant', 'heures_credit', 'date_creation')
    list_filter = ('classe', 'date_creation')
    search_fields = ('titre',)

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('cours', 'date_seance', 'lieu', 'duree_minutes')
    list_filter = ('date_seance', 'cours')
    search_fields = ('cours__titre',)

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'seance', 'statut', 'date_enregistrement')
    list_filter = ('statut', 'date_enregistrement', 'seance__cours')
    search_fields = ('etudiant__nom', 'etudiant__prenom')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'valeur', 'type_evaluation', 'date_evaluation')
    list_filter = ('type_evaluation', 'cours', 'date_evaluation')
    search_fields = ('etudiant__nom', 'cours__titre')

@admin.register(ContenuPedagogique)
class ContenuAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'type_contenu', 'date_creation')
    list_filter = ('type_contenu', 'cours', 'date_creation')
    search_fields = ('titre', 'cours__titre')

@admin.register(SuiviEtudiant)
class SuiviAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'taux_presence', 'note_generale', 'date_derniere_mise_a_jour')
    list_filter = ('cours', 'date_derniere_mise_a_jour')
    search_fields = ('etudiant__nom', 'cours__titre')
    readonly_fields = ('date_derniere_mise_a_jour',)