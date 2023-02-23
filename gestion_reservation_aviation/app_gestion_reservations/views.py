from django.shortcuts import render
from django.http  import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import LoginForm
from django import forms

# Create your views here.
def index(request):
    return HttpResponse("Hello World !")

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