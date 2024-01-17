from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient

class PatientRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    second_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120)
    pesel = forms.CharField(max_length=12)
    phone_number = forms.CharField(max_length=9)
    city = forms.CharField(max_length=120)
    street = forms.CharField(max_length=120)
    house_number = forms.CharField(max_length=120)
    zip_code = forms.CharField(max_length=6)

    class Meta(UserCreationForm.Meta):
        model = Patient
        fields = ('email', 'password1', 'password2', 'second_name', 'last_name', 'pesel', 'birth_date', 'phone_number', 'city', 'street', 'house_number', 'zip_code')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()

        return user