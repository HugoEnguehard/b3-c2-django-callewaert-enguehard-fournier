# Generated by Django 4.1.7 on 2023-02-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_gestion_reservations', '0003_user_user_id_ecole'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_email',
            field=models.CharField(max_length=100, null=True),
        ),
    ]