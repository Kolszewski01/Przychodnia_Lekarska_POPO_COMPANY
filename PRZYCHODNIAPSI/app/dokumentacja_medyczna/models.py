from django.db import models
from pacjent.models import Pacjent
from pracownik.models import Lekarz
from wizyta.models import Recepta


# Create your models here.

class Dokumentacja_medyczna(models.Model):
    pacjent = models.ForeignKey(Pacjent, on_delete=models.CASCADE)
    lekarz_wystawiajacy = models.ForeignKey(Lekarz, on_delete=models.CASCADE)
    recepta = models.ForeignKey(Recepta, on_delete=models.CASCADE)
    alergie = []
    historia_choroby = models.TextField()
    operacje = models.CharField(max_length=255)
    szczepienia = []
    wyniki_badan = models.TextField()  # Popraw nazwę pola

    zalecenia_lekarskie = models.TextField()
