from django.shortcuts import render
from django.http  import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import LoginForm, ReservationForm
from django import forms

# Create your views here.
def index(request):
    return HttpResponse("Hello World !")

def school(request, id):
    #TODO get user from cookie
    user_id = 1
    if User.objects.filter(id=user_id).exists() == False:
        return render(request, 'school.html', {'error':"User invalide"})

    #TODO TEMP
    user = User.objects.get(id=user_id)

    if user.user_type_user != 1:
        return render(request, 'school.html', {'error':"Vous ne pouvez pas accéder à cette page"})

    cours = None
    if Cour.objects.filter(id_ecole_id=id).exists() == False:
        return render(request, 'school.html', {'error':"Aucune école n'a cet id"}) 
    cours = Cour.objects.filter(id_ecole_id=id)
    #TODO if possible, don't print already taken course
    cour_choices = []
    for c in cours:
        if Reservation.objects.filter(id_cour_id=c.id, id_user_id=user.id).exists():
            continue
        cour_choices.append((c.id, c.cour_nom))
            
    #check if there is some course, if not return error
    if len(cour_choices) <= 0:
        return render(request, 'school.html', {'error':"Aucun cours pour cette école ou vous vous êtes déjà inscrit à tous les cours"})

    if request.method == ('POST'):

        form = ReservationForm(request.POST, cour_choices=cour_choices,user_id=user_id)

        if form.is_valid():
            cour = Cour.objects.get(id=form.cleaned_data['id_cour'])
            if Reservation.objects.filter(id_cour=cour.id, id_user=user.id).exists():
                form2 = ReservationForm(cour_choices=cour_choices, user_id=user_id)  
                return render(request, 'school.html', {'form':form2,'error':"Vous ne pouvez pas faire deux fois la meme réservation"})

            reservation = Reservation.objects.create(
                reservation_date=form.cleaned_data['reservation_date'],
                id_user=user,
                id_cour=cour,
            )
        return render(request, 'school.html', {'success':"Réservation réalisée avec succès"})
    else:
        form = ReservationForm(cour_choices=cour_choices, user_id=user_id)  
        return render(request, 'school.html', {'form': form})
def login(request):
    # We check if the user is already connected
    if getCookieData(request) is not None:
        return HttpResponseRedirect('/app_gestion_reservations/accueil/')
    
    # We check if the form submitted is a POST method and if it is valid compared to our template User
    submitted = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save() 
            # We check if the user exists in the database
            if User.objects.filter(user_email = form.cleaned_data['user_email'].upper()).exists():
                # We check if the password associated to the user is correct
                # TODO ENCRYPT PASSWORD
                if User.objects.filter(user_email = form.cleaned_data['user_email'].upper(), user_password = form.cleaned_data['user_password']).exists():
                    # The user is connected
                    user = User.objects.filter(user_email = form.cleaned_data['user_email'].upper(), user_password = form.cleaned_data['user_password'])[0]

                    # We prepare the redirection and we create a cookie so other pages can know if the user is logged in
                    response = HttpResponseRedirect('/app_gestion_reservations/accueil/')
                    setCookie(response, user.getAllData())
                    return response
                else: 
                    print("PASSWORD INCORRECT")
                    return render(request, 'login/login.html', {'form': form, 'error_message': "Mot de passe incorrecte" })
            else:
                print("NO SUCH USER")
                return render(request, 'login/login.html', {'form': form, 'error_message': "Ce compte n'existe pas" })
    else: 
        # If the form method is not "POST" for some reason
        form = LoginForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'login/login.html', {'form': form })


def setCookie(res, user_data):
    # Create a cookie with user infos
    res.set_cookie("logged_user", user_data, max_age = 604_800)

def getCookieData(req):
    # Get a cookie with user infos
    if "logged_user" in req.COOKIES:
        return req.COOKIES["logged_user"]
    else: 
        return None

def getUserFromEmail(email):
    return User.objects.filter(user_email = email.upper())
