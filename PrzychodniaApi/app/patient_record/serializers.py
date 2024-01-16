from rest_framework import serializers
from .models import PatientRecord, Prescription

class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRecord
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
