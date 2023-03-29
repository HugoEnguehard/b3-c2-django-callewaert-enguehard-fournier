# Generated by Django 4.1.7 on 2023-03-14 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cour_nom', models.CharField(max_length=128)),
                ('cour_date_debut', models.DateTimeField(verbose_name='Date de début du cour')),
                ('cour_date_fin', models.DateTimeField(verbose_name='Date de fin du cour')),
                ('cour_nombre_places', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ecole',
            fields=[
                ('ecole_id', models.IntegerField(primary_key=True, serialize=False)),
                ('ecole_nom', models.CharField(max_length=128)),
                ('ecole_adresse', models.CharField(max_length=128)),
                ('ecole_ville', models.CharField(max_length=128)),
                ('ecole_cp', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_nom', models.CharField(max_length=64, null=True)),
                ('user_prenom', models.CharField(max_length=64, null=True)),
                ('user_email', models.CharField(max_length=100, null=True)),
                ('user_date_naissance', models.DateTimeField(null=True, verbose_name='Date de naissance')),
                ('user_password', models.CharField(max_length=100, null=True)),
                ('user_type_user', models.IntegerField(null=True)),
                ('user_id_ecole', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_gestion_reservations.ecole')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateTimeField(verbose_name='Date de la réservation')),
                ('id_cour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gestion_reservations.cour')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gestion_reservations.user')),
            ],
        ),
        migrations.AddField(
            model_name='cour',
            name='id_ecole',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gestion_reservations.ecole'),
        ),
    ]
