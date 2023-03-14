from django.shortcuts import render
from django.http  import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return render('login')

def accueil(request):
    ecoles = Ecole.objects.all()
    cours = Cour.objects.all()
    return render(request, 'accueil/accueil.html', {'ecoles': ecoles, 'cours': cours })

def reservation(request):
    reservations = Reservation.objects.all()
    ecoles = Ecole.objects.all()
    cours = Cour.objects.all()
    return render(request, 'reservation/reservation.html', {'reservations': reservations, 'cours': cours, 'ecoles': ecoles})