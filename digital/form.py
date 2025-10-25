from django import forms
from .models import Etudiant, Classe, Cours, Seance, Presence, Note, ContenuPedagogique

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'niveau']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la classe (ex: L1-Informatique)'
            }),
            'niveau': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Niveau (ex: Licence 1)'
            }),
        }

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['numero_matricule', 'nom', 'prenom', 'email', 'classe', 'statut']
        widgets = {
            'numero_matricule': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro matricule unique'
            }),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'description', 'classe', 'heures_credit']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'heures_credit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['cours', 'date_seance', 'duree_minutes', 'lieu']
        widgets = {
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'date_seance': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duree_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['etudiant', 'seance', 'statut', 'remarque']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-control'}),
            'seance': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'remarque': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['etudiant', 'cours', 'valeur', 'type_evaluation', 'commentaire']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-control'}),
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'valeur': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.5,
                'min': 0,
                'max': 20
            }),
            'type_evaluation': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class ContenuForm(forms.ModelForm):
    class Meta:
        model = ContenuPedagogique
        fields = ['cours', 'titre', 'description', 'type_contenu', 'lien_fichier', 'lien_externe']
        widgets = {
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'type_contenu': forms.Select(attrs={'class': 'form-control'}),
            'lien_fichier': forms.FileInput(attrs={'class': 'form-control'}),
            'lien_externe': forms.URLInput(attrs={'class': 'form-control'}),
        }