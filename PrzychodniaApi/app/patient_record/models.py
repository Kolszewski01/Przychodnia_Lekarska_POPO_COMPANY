from django.db import models
from patient.models import Patient

# Create your models here.
class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allergies = models.TextField()
    medical_history = models.TextField()
    visit_notes = models.TextField()
    operations = models.TextField()
    vaccinations = models.TextField()
    test_results = models.TextField()

    def __str__(self):
        return str(self.patient)

class Prescription(models.Model):
    patient_record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    additional_instructions = models.TextField(blank=True, null=True)
    prescribed_date = models.DateField()
