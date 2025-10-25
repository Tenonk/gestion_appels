from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Vues temporaires
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'classes': 3, 'etudiants': 85, 'cours': 12, 'seances': 36,
        'user': request.user, 'mes_cours_count': 5, 'mes_seances_count': 15,
        'mes_classes_count': 2, 'recent_seances': [], 'mes_seances_recentes': []
    })

@login_required
def liste_classes(request):
    return render(request, 'classes/liste.html', {'classes': []})

@login_required
def liste_etudiants(request):
    return render(request, 'etudiants/liste.html', {'etudiants': []})

@login_required
def liste_cours(request):
    return render(request, 'cours/liste.html', {'cours': []})

@login_required
def liste_seances(request):
    return render(request, 'appels/liste.html', {'seances': []})

@login_required
def creer_classe(request):
    return render(request, 'classes/form.html')

@login_required
def creer_etudiant(request):
    return render(request, 'etudiants/form.html')

@login_required
def creer_cours(request):
    return render(request, 'cours/form.html')

@login_required
def detail_classe(request, id):
    return render(request, 'classes/detail.html')

@login_required
def detail_etudiant(request, id):
    return render(request, 'etudiants/detail.html')

@login_required
def detail_cours(request, id):
    return render(request, 'cours/detail.html')

@login_required
def modifier_etudiant(request, id):
    return render(request, 'etudiants/form.html')

@login_required
def faire_appel(request, seance_id):
    return render(request, 'appels/faire_appel.html')