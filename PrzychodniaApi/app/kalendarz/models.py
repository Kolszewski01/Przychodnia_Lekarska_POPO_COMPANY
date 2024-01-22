from django.db import models
from patient.models import Patient
from worker.models import Doctor

# Create your models here.

class Calendar(models.Model):
    data = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.doctor} - {self.data}"

class Reservation(models.Model):
    data = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Rezerwacja dla {self.patient} u {self.doctor} - {self.data}"

