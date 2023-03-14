from django.urls import path, re_path
from . import views

urlpatterns = [
    path('school/<int:id>', views.school, name="School"),    
    path('', views.login, name="Login"),
]
