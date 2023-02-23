from django.shortcuts import render
from django.http  import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import LoginForm
from django import forms

# Create your views here.
def index(request):
    return HttpResponse("Hello World !")

def login(request):
    submitted = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save() 
            print(form.cleaned_data['user_email'])
            if User.objects.filter(user_email = form.cleaned_data['user_email']):
                if User.objects.filter(user_email = form.cleaned_data['user_email'], user_password = form.cleaned_data['user_password']).exists():
                    print("USER CONNECTED")
                    return HttpResponseRedirect('/app_gestion_reservations/accueil/')
                else: 
                    print("PASSWORD INCORRECT")
            else:
                print("NO SUCH USER")
            
    else: 
        form = LoginForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'login/login.html', {'form': form})
