# b3-c2-django-callewaert-enguehard-fournier
Application de gestion des réservations pour les écoles de pilotage.

# Start project 
cd b3-c2-django-callewaert-enguehard-fournier/gestion_reservation_aviation
python ./manage.py runserver

# Accèder à l'application
Dans un navigateur entrer l'url : http://127.0.0.1:8000/app_gestion_reservations/

Pour accèder à la partie admin : http://127.0.0.1:8000/admin/

# SUPERUSER login/pswd
login : admin
password : password

# Types d'utilisateur
- Élève => 
    - Faire une réservation pour un cour dans une école
    - Consulter les détails de sa réservation
    - Annuler sa réservation
- École =>
    - Consulter les cours et les participants de chaque cour pour son établissement
    - OPTIONNEL : Annuler un cour
    - OPTIONNEL : Annuler une réservation

# Tables
- users => 
    - nom => string(64)
    - prenom => string(64)
    - email => string(256)
    - date_naissance => date
    - type_user => int(1)
        - 0 : admin 
        - 1 : eleve
        - 2 : ecole

- ecoles =>
    - nom => string(128)
    - adresse => string(128)
    - ville => string(128)
    - cp = string(5)

- cours => 
    - nom => string(128)
    - date_debut => date
    - date_fin => date
    - nombre_places => int(3)
    - CLE ETRANGERE : id_ecole

- reservations =>
    - date => (date)
    - CLE ETRANGERE : id_user
    - CLE ETRANGERE : id_cours

# Pages
- Login =>
    - Formulaire de connexion

- Register => 
    - Formulaire d'inscription

- Accueil => 
    - USER 1 : Liste des écoles 
        - Si clique sur une école => Redirige vers la vue "École"
    - USER 2 : Liste des cours 
        - Si clique sur un cour => Liste des réservations

- École => 
    - USER 1 : Liste des cours réservables

- Réservations =>
    - USER 1 : Liste de ses réservations 
        - Possibilité de consulter en détail une réservation
        - Possibilité de supprimer une réservation