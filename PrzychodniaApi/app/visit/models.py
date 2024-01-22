from django.db import models
from worker.models import Doctor
from patient.models import Patient
from kalendarz.models import Reservation

class Visit(models.Model):
    reservation_copy = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=50, choices=[('scheduled', 'Scheduled'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='scheduled')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor.specialization} - {self.reservation_copy.data} - {self.patient}"