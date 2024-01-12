from rest_framework import serializers
from .models import Pacjent

class PacjentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pacjent
        fields = ['id','PESEL','name','second_name','surname','phone_number']