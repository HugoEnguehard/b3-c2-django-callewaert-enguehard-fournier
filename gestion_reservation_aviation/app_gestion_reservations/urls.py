from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.login, name="Login"),
    path('register/', views.register, name="Register"),
    path('accueil/', views.accueil, name="Accueil"),
    path('school/<int:id>', views.school, name="School"),    
    path('reservation/', views.reservation, name="Reservation"),
]
