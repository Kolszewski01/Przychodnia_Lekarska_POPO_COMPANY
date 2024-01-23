from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from worker.models import Doctor
from patient.models import Patient
from kalendarz.models import Reservation

class Visit(models.Model):
    reservation_copy = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=50, choices=[('zaplanowana', 'Zaplanowana'), ('odwołana', 'Odwołana'), ('zakończona', 'Zakończona')], default='zaplanowana')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reservation_date = models.DateField(null=True)  # Dodaj pole do przechowywania daty rezerwacji

    def __str__(self):
        return f"{self.doctor.specialization} - {self.reservation_copy.data} - {self.patient}"

@receiver(post_delete, sender=Reservation)
def on_reservation_delete(sender, instance, **kwargs):
    # Po usunięciu rezerwacji, zaktualizuj datę wizyty na NULL w modelu Visit
    Visit.objects.filter(reservation_copy=instance).update(reservation_date=None)
