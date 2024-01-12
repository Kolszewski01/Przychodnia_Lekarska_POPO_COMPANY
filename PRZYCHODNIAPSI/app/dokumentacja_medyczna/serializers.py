from rest_framework import serializers
from .models import Dokumentacja_medyczna
from pacjent.serializers import PacjentSerializer
from pracownik.serializers import LekarzSerializer, PracownikSerializer
from wizyta.serializers import ReceptaSerializer


class Dokumentacja_medycznaSerializer(serializers.HyperlinkedModelSerializer):
    pacjent = PacjentSerializer()
    lekarz_wystawiajacy = LekarzSerializer()
    recepta = ReceptaSerializer()

    class Meta:
        model = Dokumentacja_medyczna
        fields = ['id', 'pacjent', 'lekarz_wystawiajacy', 'recepta',
                  'alergie', 'historia_choroby', 'operacje', 'szczepienia',
                  'wyniki_badan', 'zalecenia_lekarskie']
