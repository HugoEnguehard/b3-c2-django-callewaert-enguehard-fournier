from django import forms
from datetime import datetime
from .models import Reservation, Cour, User
class ReservationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cour_choices = kwargs.pop('cour_choices', 1)
        user_id = kwargs.pop('user_id', 1)
        super().__init__(*args, **kwargs)
        self.fields['reservation_date'] = forms.DateTimeField(widget = forms.HiddenInput(),initial=datetime.now())
        self.fields['id_user'] = forms.IntegerField(widget = forms.HiddenInput(), required = False, initial=user_id)
        self.fields['id_cour'] = forms.ChoiceField(choices=cour_choices)
        
class LoginForm(forms.Form):
    user_email = forms.CharField(max_length=100, widget=forms.EmailInput())
    user_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = User
    
