# Generated by Django 4.1.7 on 2023-02-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_gestion_reservations', '0005_user_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_date_naissance',
            field=models.DateTimeField(null=True, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_nom',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_prenom',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type_user',
            field=models.IntegerField(null=True),
        ),
    ]
