from django.db import models

# Create your models here.
class Pacjent(models.Model):
    PESEL = models.CharField(max_length=11)
    name = models.CharField(max_length=45)
    second_name = models.CharField(max_length=45, blank=True)
    surname = models.CharField(max_length=45)
    phone_number = models.IntegerField()

    def __str__(self):
        return (f'{self.name} {self.surname}')