from django.db import models
from patient.models import Patient
from worker.models import Doctor

# Create your models here.

class Calendar(models.Model):
    data = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

class Reservation(models.Model):
    data = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
