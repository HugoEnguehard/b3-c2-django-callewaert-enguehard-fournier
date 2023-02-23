from django import forms 
from .models import User

class LoginForm(forms.Form):
    user_email = forms.CharField(max_length=100, widget=forms.EmailInput())
    user_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = User
    