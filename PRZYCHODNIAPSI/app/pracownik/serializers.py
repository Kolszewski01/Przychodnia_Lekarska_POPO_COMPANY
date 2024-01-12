from rest_framework import serializers
from .models import Pracownik, Lekarz


class PracownikSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pracownik
        fields = ['id', 'name', 'second_name', 'surname', 'position']


class LekarzSerializer(serializers.HyperlinkedModelSerializer):
    pracownik = PracownikSerializer()  # Dodaj tę linię, jeśli nie masz jej wcześniej

    class Meta:
        model = Lekarz
        fields = ['id', 'pracownik', 'specialization']

