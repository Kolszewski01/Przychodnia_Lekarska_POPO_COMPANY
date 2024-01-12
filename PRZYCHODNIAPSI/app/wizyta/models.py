from django.db import models
from pracownik.models import Lekarz
from pacjent.models import Pacjent
from django.utils import timezone

STATUS_WIZYTY = (
    ('W', 'Wolny termin'),
    ('Z', 'Zajęty termin')
)


# Create your models here.
class Kalendarz(models.Model):
    termin_wizyty = models.DateTimeField(default=timezone.now)
    czy_zajety = models.CharField(choices=STATUS_WIZYTY, max_length=100, blank=True)

    def __str__(self):
        return (f'{self.termin_wizyty}')



STATUS = {
    ('Zakończono','Zakończono'),
    ('Oczekiwanie na wizytę','Oczekiwanie na wizytę'),
}


class Wizyta(models.Model):
    pacjent = models.ForeignKey(Pacjent, on_delete=models.CASCADE)
    pracownik = models.ForeignKey(Lekarz, on_delete=models.CASCADE)
    nr_sali = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=25, default="Oczekiwanie na wizytę")
    kalendarz = models.ForeignKey(Kalendarz, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return (f'{self.pacjent}, {self.pracownik}, {self.status}, nr sali: {self.nr_sali}, {self.kalendarz}')


ZAPLATA_WIZYTA = (
    ('karta', 'Płatność kartą'),
    ('gotówka', 'Płatność gotówką')
)


class Paragon(models.Model):
    wizyta = models.ForeignKey(Wizyta, on_delete=models.CASCADE)
    kwota = models.FloatField()
    metoda_platnosci = models.CharField(choices=ZAPLATA_WIZYTA, max_length=100)
    nazwa_uslugi = models.CharField(max_length=255)
    data_wydania = models.DateTimeField()


class Recepta(models.Model):
    wizyta = models.ForeignKey(Wizyta, on_delete=models.CASCADE)
    data_wystawienia = models.DateTimeField()
    dawkowanie = models.CharField(max_length=255)
    leki = []
