from django.shortcuts import render
from django.http  import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import LoginForm, ReservationForm
from django import forms
import ast

# Create your views here.
def index(request):
    return render('login')

def school(request, id):
    cookieValue = getCookieData(request)

    pathToSchoolFile = "school/school.html"
    if cookieValue is None:
        return HttpResponseRedirect('/app_gestion_reservations/')

    if Ecole.objects.filter(id=id).exists() == False:
        return render(request, pathToSchoolFile, {'error':"Aucune école n'a cet id"}) 
    school = Ecole.objects.filter(id=id)[0]

    if cookieValue['user_email'] : 
        if User.objects.filter(user_email=cookieValue['user_email']).exists() == False:
            return render(request, pathToSchoolFile, {'error':"User invalide"})

    user = User.objects.filter(user_email=cookieValue['user_email'])[0]
    
    if Cour.objects.filter(id_ecole_id=id).exists() == False:
        return render(request, pathToSchoolFile, {'error':"Cette école n'a aucun cours"}) 
    
    cours = Cour.objects.filter(id_ecole_id=id)
    
    cour_choices = []
    for c in cours:
        if Reservation.objects.filter(id_cour_id=c.id, id_user_id=user.id).exists():
            continue
        cour_choices.append((c.id, c.cour_nom))

    reservations = []
    print("HEEEEERE", user.user_type_user)
    if user.user_type_user == 2:
        for c in cours:
            if Reservation.objects.filter(id_cour_id=c.id).exists() == False:
                continue
            reservation = Reservation.objects.filter(id_cour_id=c.id)
            for r in reservation:
                reservations.append({"course_name" : c.cour_nom, "reservation_id":r.id, "user_name":r.id_user.user_nom, "user_id":r.id_user, "reservation_date":r.reservation_date, "start_course_date":c.cour_date_debut, "end_course_date":c.cour_date_debut})

    if len(cour_choices) <= 0:
        return render(request, pathToSchoolFile, {'error':"Aucun cours pour cette école ou vous vous êtes déjà inscrit à tous les cours", "school_data":school, "reservations":reservations})

    if request.method == ('POST'):

        form = ReservationForm(request.POST, cour_choices=cour_choices,user_id=user.id)

        if form.is_valid():
            cour = Cour.objects.get(id=form.cleaned_data['id_cour'])
            if Reservation.objects.filter(id_cour=cour.id, id_user=user.id).exists():
                form2 = ReservationForm(cour_choices=cour_choices, user_id=user.id)  
                return render(request, pathToSchoolFile, {'form':form2,'error':"Vous ne pouvez pas faire deux fois la meme réservation", "school_data":school, "reservations":reservations})

            reservation = Reservation.objects.create(
                reservation_date=form.cleaned_data['reservation_date'],
                id_user=user,
                id_cour=cour,
            )
        return render(request, pathToSchoolFile, {'success':"Réservation réalisée avec succès","school_data":school, "reservations":reservations})
    else:
        form = ReservationForm(cour_choices=cour_choices, user_id=user.id)  
        return render(request, pathToSchoolFile, {'form': form, "school_data":school, "reservations":reservations})
    
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
        return  ast.literal_eval(req.COOKIES["logged_user"])
    else: 
        return None

def getUserFromEmail(email):
    return User.objects.filter(user_email = email.upper())

def accueil(request):
    ecoles = Ecole.objects.all()
    cours = Cour.objects.all()
    return render(request, 'accueil/accueil.html', {'ecoles': ecoles, 'cours': cours })

def reservation(request):
    reservations = Reservation.objects.all()
    ecoles = Ecole.objects.all()
    cours = Cour.objects.all()
    return render(request, 'reservation/reservation.html', {'reservations': reservations, 'cours': cours, 'ecoles': ecoles})
