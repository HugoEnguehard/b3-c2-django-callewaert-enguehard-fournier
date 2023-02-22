import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Ecole(models.Model):
    ecole_nom = models.CharField(max_length=128)
    ecole_adresse = models.CharField(max_length=128)
    ecole_ville = models.CharField(max_length=128)
    ecole_cp = models.CharField(max_length=5)
    
    def __str__(self):
        return self.ecole_nom
    
class User(models.Model):
    user_nom = models.CharField(max_length=64)
    user_prenom = models.CharField(max_length=64)
    user_date_naissance = models.DateTimeField('Date de naissance')
    user_type_user = models.IntegerField()
    user_id_ecole = models.ForeignKey(Ecole, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_prenom} {self.user_nom} {self.user_id_ecole}"
    
class Cour(models.Model):
    cour_nom = models.CharField(max_length=128)
    cour_date_debut = models.DateTimeField('Date de début du cour')
    cour_date_fin = models.DateTimeField('Date de fin du cour')
    cour_nombre_places = models.IntegerField()
    id_ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cour_nom

class Reservation(models.Model):
    reservation_date = models.DateTimeField('Date de la réservation')
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_cour = models.ForeignKey(Cour, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.reservation_date}"
