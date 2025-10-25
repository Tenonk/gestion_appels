from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Classe(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    niveau = models.CharField(max_length=50)
    nombre_etudiants = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} ({self.niveau})"
    
    def mettre_a_jour_nombre_etudiants(self):
        """Met à jour le nombre d'étudiants actifs"""
        self.nombre_etudiants = self.etudiants.filter(statut='actif').count()
        self.save()
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

class Etudiant(models.Model):
    STATUTS = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ]
    
    numero_matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='etudiants')
    statut = models.CharField(max_length=20, choices=STATUTS, default='actif')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def taux_presence_global(self):
        """Calcule le taux de présence global de l'étudiant"""
        total_seances = Presence.objects.filter(etudiant=self).count()
        if total_seances == 0:
            return 0
        presentes = Presence.objects.filter(
            etudiant=self, 
            statut__in=['present', 'retard']
        ).count()
        return (presentes / total_seances) * 100
    
    def moyenne_generale(self):
        """Calcule la moyenne générale de l'étudiant"""
        notes = self.notes.all()
        if not notes.exists():
            return None
        return sum(n.valeur for n in notes) / notes.count()
    
    class Meta:
        ordering = ['classe', 'nom']
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"

class Cours(models.Model):
    titre = models.CharField(max_length=150)
    description = models.TextField()
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='cours')
    enseignant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cours_enseignes')
    date_creation = models.DateTimeField(auto_now_add=True)
    heures_credit = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.titre} - {self.classe}"
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

class Seance(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='seances')
    date_seance = models.DateTimeField()
    duree_minutes = models.IntegerField(default=60)
    lieu = models.CharField(max_length=100, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cours.titre} - {self.date_seance.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        ordering = ['-date_seance']
        verbose_name = "Séance"
        verbose_name_plural = "Séances"

class Presence(models.Model):
    STATUTS_PRESENCE = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('retard', 'En retard'),
        ('justifie', 'Absent justifié'),
    ]
    
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='presences')
    statut = models.CharField(max_length=20, choices=STATUTS_PRESENCE, default='absent')
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    remarque = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.etudiant} - {self.seance} : {self.get_statut_display()}"
    
    class Meta:
        unique_together = ('seance', 'etudiant')
        ordering = ['-date_enregistrement']
        verbose_name = "Présence"
        verbose_name_plural = "Présences"

class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='notes')
    valeur = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    type_evaluation = models.CharField(max_length=50, choices=[
        ('controle', 'Contrôle'),
        ('examen', 'Examen'),
        ('travail', 'Travail pratique'),
        ('participation', 'Participation'),
    ])
    date_evaluation = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.etudiant} - {self.cours} : {self.valeur}/20"
    
    class Meta:
        unique_together = ('etudiant', 'cours', 'type_evaluation')
        ordering = ['-date_evaluation']
        verbose_name = "Note"
        verbose_name_plural = "Notes"

class ContenuPedagogique(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='contenus')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_contenu = models.CharField(max_length=50, choices=[
        ('resume', 'Résumé'),
        ('exercice', 'Exercice'),
        ('td', 'Travaux Dirigés'),
        ('tp', 'Travaux Pratiques'),
        ('ressource', 'Ressource externe'),
    ])
    lien_fichier = models.FileField(upload_to='contenus/%Y/%m/%d/', blank=True)
    lien_externe = models.URLField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titre} - {self.cours}"
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Contenu Pédagogique"
        verbose_name_plural = "Contenus Pédagogiques"

class SuiviEtudiant(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='suivi')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    taux_presence = models.FloatField(default=0)
    note_generale = models.FloatField(null=True, blank=True)
    remarques_enseignant = models.TextField(blank=True)
    date_derniere_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Suivi {self.etudiant} - {self.cours}"
    
    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour calculer automatiquement les stats"""
        self.taux_presence = self.calculer_taux_presence()
        self.note_generale = self.calculer_moyenne()
        super().save(*args, **kwargs)
    
    def calculer_taux_presence(self):
        """Calcule le pourcentage de présence d'un étudiant"""
        seances = Seance.objects.filter(cours=self.cours)
        if not seances.exists():
            return 0
        presences = Presence.objects.filter(
            seance__cours=self.cours,
            etudiant=self.etudiant,
            statut__in=['present', 'retard']
        ).count()
        return (presences / seances.count()) * 100 if seances.count() > 0 else 0
    
    def calculer_moyenne(self):
        """Calcule la moyenne générale d'un étudiant"""
        notes = Note.objects.filter(etudiant=self.etudiant, cours=self.cours)
        if not notes.exists():
            return None
        return sum(n.valeur for n in notes) / notes.count()
    
    class Meta:
        unique_together = ('etudiant', 'cours')
        verbose_name = "Suivi Étudiant"
        verbose_name_plural = "Suivi Étudiants"