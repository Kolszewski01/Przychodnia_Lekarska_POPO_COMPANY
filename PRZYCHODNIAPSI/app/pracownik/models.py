from django.db import models


# Create your models here.
class Pracownik(models.Model):
    name = models.CharField(max_length=45)
    second_name = models.CharField(max_length=45, default='')
    surname = models.CharField(max_length=45)
    position = models.CharField(max_length=45)

    def __str__(self):
        return (f'{self.name} {self.surname}')


class Lekarz(models.Model):
    pracownik = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=45)

    def __str__(self):
        return (f'{self.pracownik}')
