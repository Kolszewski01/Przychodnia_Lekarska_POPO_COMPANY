# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pesel = models.CharField(max_length=11, unique=True)
    imie = models.CharField(max_length=30)
    drugie_imie = models.CharField(max_length=30, blank=True, null=True)
    nazwisko = models.CharField(max_length=30)
    nr_telefonu = models.CharField(max_length=15)
    miejscowosc = models.CharField(max_length=50)
    ulica = models.CharField(max_length=50)
    nr_domu = models.CharField(max_length=10)
    kod_pocztowy = models.CharField(max_length=10)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Zmiana related_name dla groups
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Zmiana related_name dla user_permissions
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.username})"
