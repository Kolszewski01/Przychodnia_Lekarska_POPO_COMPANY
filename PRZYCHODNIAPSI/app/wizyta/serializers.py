from rest_framework import serializers
from .models import Wizyta, Paragon, Recepta, Kalendarz
from pracownik.serializers import LekarzSerializer
from pacjent.serializers import PacjentSerializer


class KalendarzSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kalendarz
        fields = ['id', 'termin_wizyty', 'czy_zajety']


class WizytaSerializer(serializers.HyperlinkedModelSerializer):
    pracownik = LekarzSerializer()
    pacjent = PacjentSerializer()
    kalendarz = KalendarzSerializer()

    class Meta:
        model = Wizyta
        fields = ['id', 'pacjent', 'pracownik', 'nr_sali', 'status', 'kalendarz']


class ParagonSerializer(serializers.HyperlinkedModelSerializer):
    wizyta = WizytaSerializer()

    class Meta:
        model = Paragon
        fields = ['id', 'wizyta', 'kwota', 'metoda_platnosci', 'nazwa_uslugi', 'data_wydania']


class ReceptaSerializer(serializers.HyperlinkedModelSerializer):
    wizyta = WizytaSerializer()

    class Meta:
        model = Recepta
        fields = ['id', 'wizyta', 'data_wystawienia', 'dawkowanie', 'leki']
