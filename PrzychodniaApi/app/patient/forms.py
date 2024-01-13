from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient

class PatientRegistrationForm(UserCreationForm):
    second_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120)
    pesel = forms.CharField(max_length=12)
    birth_date = forms.DateField()
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
        user.is_patient = True  # Oznaczamy użytkownika jako pacjenta
        user.save()
        #
        # patient = Patient.objects.create(
        #     user=user,
        #     second_name=self.cleaned_data.get('second_name'),
        #     last_name=self.cleaned_data['last_name'],
        #     pesel=self.cleaned_data['pesel'],
        #     birth_date=self.cleaned_data['birth_date'],
        #     phone_number=self.cleaned_data['phone_number'],
        #     city=self.cleaned_data['city'],
        #     street=self.cleaned_data['street'],
        #     house_number=self.cleaned_data['house_number'],
        #     zip_code=self.cleaned_data['zip_code'],
        # )
        return user