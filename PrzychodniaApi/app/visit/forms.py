from django import forms
from .models import Visit

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['reservation_copy', 'doctor', 'room_number', 'status', 'price', 'patient']