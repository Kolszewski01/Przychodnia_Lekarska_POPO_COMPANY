from django.db import models


# Create your models here.

class Calendar(models.Model):
    data = models.DateTimeField()


class Reservation(models.Model):
    data = models.DateField()


