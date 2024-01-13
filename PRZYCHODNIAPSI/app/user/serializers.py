from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'pesel', 'imie',
                  'drugie_imie', 'nazwisko', 'nr_telefonu', 'miejscowosc',
                  'ulica', 'nr_domu', 'kod_pocztowy']