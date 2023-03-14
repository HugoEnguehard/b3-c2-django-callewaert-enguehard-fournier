from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('accueil/', views.accueil, name="Accueil"),
    path('reservation/', views.reservation, name="Reservation"),
]
