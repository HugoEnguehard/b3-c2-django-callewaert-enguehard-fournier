from django.shortcuts import render
from django.http  import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import LoginForm, RegisterForm
from django import forms
import ast
import bcrypt

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
        # If the request method is not "POST" for some reason
        form = LoginForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'login/login.html', {'form': form })

def register(request):
    # We check if the user is already connected
    if getCookieData(request) is not None:
        return HttpResponseRedirect('/app_gestion_reservations/accueil/')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            # print(form.cleaned_data)
            if(form.cleaned_data["user_password"] != form.cleaned_data["user_confirm_password"]):
                print("PASSWORD INCORRECT")
                return render(request, 'register/register.html', {'form': form, 'error_message': "Les mots de passe ne sont pas identiques" })
            if(form.cleaned_data["user_type_user"] == "2" and form.cleaned_data["user_id_ecole"] is None):
                print("SCHOOL USER MUST BE ASSOCIATED WITH A SCHOOL")
                return render(request, 'register/register.html', {'form': form, 'error_message': "Un utilisateur de type \"École\" doit être associé à une école" })
            if(form.cleaned_data["user_type_user"] == "1" and form.cleaned_data["user_id_ecole"] is not None):
                print("STUDENT USER MUST NOT BE ASSOCIATED WITH A SCHOOL")
                return render(request, 'register/register.html', {'form': form, 'error_message': "Un utilisateur de type \"Élève\" ne doit pas être associé à une école" })
            
            # Vérifier que le USER n'existe pas (via email)
            if User.objects.filter(user_email = form.cleaned_data['user_email'].upper()).exists():
                print("USER ALREADY EXISTS")
                return render(request, 'register/register.html', {'form': form, 'error_message': "Cet adresse email est déjà associée à un compte" })
            
            # Hashage du mot de passe
            hashedPassword =  bcrypt.hashpw(form.cleaned_data["user_password"].encode('utf-8'), bcrypt.gensalt())
            
            # Création de l'objet User que l'on va ajouter dans la base de données avec le mdp hashé
            new_user = User(user_nom=form.cleaned_data["user_nom"], user_prenom= form.cleaned_data["user_prenom"], user_email= form.cleaned_data["user_email"].upper(), user_date_naissance= form.cleaned_data["user_date_naissance"], user_password= hashedPassword.decode('utf-8'), user_type_user= form.cleaned_data["user_type_user"], user_id_ecole= form.cleaned_data["user_id_ecole"])
            
            # Sauvegarde du User dans la base de données
            new_user.save()
            
            # Redirection vers la page de Login
            return HttpResponseRedirect('/app_gestion_reservations/')
            
            
    else:
        # If the request method is not "POST" for some reason
        form = RegisterForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'register/register.html', {'form': form})
    
    
    
    

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