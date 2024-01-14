from django.db import models
from user.models import User


class Worker(User):
    EMPLOYMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('inactive', 'Inactive'),
    ]

    employment_status = models.CharField(max_length=10, choices=EMPLOYMENT_STATUS_CHOICES, default='active')
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=120)
    house_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='static/images/profile_images', null=True, blank=True)

    class Meta:
        abstract = True


class Doctor(Worker):
    specialization = models.CharField(max_length=120)
    room_number = models.CharField(max_length=10, verbose_name='Room Number')

class Secretary(Worker):
    pass

