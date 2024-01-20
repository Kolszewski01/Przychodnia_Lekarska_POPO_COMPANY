from django import forms
from .models import Prescription,PatientRecord

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'




class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['allergies', 'medical_history', 'visit_notes', 'operations', 'vaccinations', 'test_results']
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'visit_notes': forms.Textarea(attrs={'rows': 3}),
            'operations': forms.Textarea(attrs={'rows': 3}),
            'vaccinations': forms.Textarea(attrs={'rows': 3}),
            'test_results': forms.Textarea(attrs={'rows': 3}),
        }