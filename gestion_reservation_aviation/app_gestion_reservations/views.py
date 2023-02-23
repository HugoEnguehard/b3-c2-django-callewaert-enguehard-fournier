from django.shortcuts import render
from django.http  import HttpResponse
from .models import *
from django.core import serializers
from .forms import ReservationForm
# assuming obj is a model instance
# Create your views here.
def index(request):
    return HttpResponse("Hello World !")

def school(request, id):
    #TODO get user
    
    user_id = 1
    if User.objects.filter(id=user_id).exists() == False:
        return render(request, 'school.html', {'error':"User invalide"})
    #TODO get user_object

    #TODO TEMP
    user = User.objects.get(id=user_id)

    if user.user_type_user != 1:
        return render(request, 'school.html', {'error':"Vous ne pouvez pas accéder à cette page"})

    cours = None
    if Cour.objects.filter(id_ecole_id=id).exists() == False:
        return render(request, 'school.html', {'error':"Aucune école n'a cet id"}) 
    cours = Cour.objects.filter(id_ecole_id=id)
    cour_choices = [(c.id, c.cour_nom) for c in cours]
    #check if there is some course, if not return error
    if len(cour_choices) <= 0:
        return render(request, 'school.html', {'error':"Aucun cours pour cette école"})

    if request.method == ('POST'):
        form = ReservationForm(request.POST, cour_choices=cour_choices,user_id=user_id)
        
        if form.is_valid():
            cour = Cour.objects.get(id=form.cleaned_data['id_cour'])
            reservation = Reservation.objects.create(
                reservation_date=form.cleaned_data['reservation_date'],
                id_user=user,
                id_cour=cour,
            )
        return render(request, 'school.html', {'success':"Réservation réalisée"})
    else:
        form = ReservationForm(cour_choices=cour_choices, user_id=user_id)  
        return render(request, 'school.html', {'form': form})