from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Ecole)
admin.site.register(Cour)
admin.site.register(Reservation)