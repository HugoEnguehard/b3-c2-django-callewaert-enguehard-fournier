import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Ecole(models.Model):
    ecole_id = models.IntegerField(primary_key=True)
    ecole_nom = models.CharField(max_length=128)
    ecole_adresse = models.CharField(max_length=128)
    ecole_ville = models.CharField(max_length=128)
    ecole_cp = models.CharField(max_length=5)
    
    def __str__(self):
        return self.ecole_nom
    
    def getDataForForm(self):
        return {
            "id_ecole" : self.ecole_id,
            "nom_ecole" : self.ecole_nom,
        }
    
class User(models.Model):
    user_nom = models.CharField(max_length=64, null=True)
    user_prenom = models.CharField(max_length=64, null=True)
    user_email = models.CharField(max_length=100, null=True)
    user_date_naissance = models.DateTimeField('Date de naissance', null=True)
    user_password = models.CharField(max_length=100, null=True)
    user_type_user = models.IntegerField(null=True)
    user_id_ecole = models.ForeignKey(Ecole, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_email} {self.user_id_ecole}"
    
    def getAllData(self):
        return {
            "user_nom" : self.user_nom,
            "user_prenom" : self.user_prenom,
            "user_email" : self.user_email,
            "user_type_user" : self.user_type_user,
            "user_id_ecole" : self.user_id_ecole,
        }
    
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
