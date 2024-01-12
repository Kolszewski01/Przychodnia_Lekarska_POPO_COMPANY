from django.contrib import admin

# Register your models here.
from .models import Wizyta, Paragon, Recepta, Kalendarz

admin.site.register(Wizyta)
admin.site.register(Paragon)
admin.site.register(Recepta)
admin.site.register(Kalendarz)
