from django.contrib import admin
from .models import PatientRecord,Prescription
# Register your models here.
admin.site.register(PatientRecord)
admin.site.register(Prescription)
