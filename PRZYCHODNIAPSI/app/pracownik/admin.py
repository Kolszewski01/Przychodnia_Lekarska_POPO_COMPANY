from django.contrib import admin

# Register your models here.
from .models import Pracownik, Lekarz

admin.site.register(Pracownik)
admin.site.register(Lekarz)
