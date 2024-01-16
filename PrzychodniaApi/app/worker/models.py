from django.db import models
from user.models import User


class Worker(User):
    EMPLOYMENT_STATUS_CHOICES  = [
        ('aktywny', 'Aktywny'),
        ('na_urlopie', 'Na Urlopie'),
        ('nieaktywny', 'Nieaktywny'),
    ]

    employment_status = models.CharField(choices=EMPLOYMENT_STATUS_CHOICES, default='Aktywny')
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=120)
    house_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='static/images/profile_images', null=True, blank=True)
    is_worker = models.BooleanField(default=True)
    class Meta:
        abstract = True


class Doctor(Worker):
    PROF_TITLE_CHOICES = [
        ('MD', 'Doktor medycyny'),
        ('PhD', 'Doktor nauk medycznych'),
        ('Prof.', 'Profesor'),
        ('Dr hab. med.', 'Doktor habilitowany medycyny'),
        ('Spec.', 'Specjalista'),
        ('Asystent', 'Młodszy lekarz'),
        ('Doc.', 'Docent'),
        ('Doc. hab.', 'Doktor habilitowany'),
        ('Doc. dr', 'Doktor habilitowany nauk medycznych'),
        ('Dr. med.', 'Doktor medycyny'),
        ('Kier. lab.', 'Kierownik laboratorium'),
        ('Prof. dr hab. med.', 'Profesor doktor habilitowany medycyny'),
        ('Doc. dr hab. med.', 'Docent doktor habilitowany medycyny'),
        ('Dr n. med.', 'Doktor nauk medycznych'),
        ('Dr inż.', 'Doktor inżynier'),
        ('Dr med. vet.', 'Doktor medycyny weterynaryjnej'),
        ('Dr dent.', 'Doktor stomatologii')
    ]

    specialization = models.CharField(max_length=120)
    room_number = models.CharField(max_length=10, verbose_name='Room Number')
    prof_title = models.CharField(choices=PROF_TITLE_CHOICES, default='Dr. med.')

class Secretary(Worker):
    pass

