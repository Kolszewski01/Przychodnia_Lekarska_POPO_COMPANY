from django.db import models

from user.models import User


# Create your models here.

class Patient(User):
    second_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120)
    pesel = models.CharField(max_length=12)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=120)
    house_number = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.name} {self.last_name} PESEL: {self.pesel}'




