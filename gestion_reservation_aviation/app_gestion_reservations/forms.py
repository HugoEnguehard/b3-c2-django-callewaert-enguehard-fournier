from django import forms 
from .models import User, Ecole
from django.contrib.admin.widgets import AdminDateWidget

class LoginForm(forms.Form):
    user_email = forms.CharField(max_length=100, widget=forms.EmailInput())
    user_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = User
        

class RegisterForm(forms.Form):
    user_nom = forms.CharField(max_length=100)
    user_prenom = forms.CharField(max_length=100)
    user_email = forms.CharField(max_length=100, widget=forms.EmailInput())
    user_date_naissance = forms.DateField(widget=AdminDateWidget)
    user_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    user_confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    user_type_user = forms.ChoiceField(choices=(
        ("1", "Élève"),
        ("2", "École")
    ))
    user_id_ecole = forms.ModelChoiceField(queryset=Ecole.objects.all(), required=False)
    
    class Meta:
        model = User
    
    