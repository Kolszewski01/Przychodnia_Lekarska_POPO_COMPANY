from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, Secretary

class DoctorRegistrationForm(UserCreationForm):
    specialization = forms.CharField(max_length=120)
    room_number = forms.CharField(max_length=10, label='Room Number')
    prof_title = forms.ChoiceField(choices=Doctor.PROF_TITLE_CHOICES, initial='Dr. med.')

    role = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('secretary', 'Secretary'), ('patient', 'Patient')],
                             initial='doctor', label='Role')

    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = (
        'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'city', 'street', 'house_number',
        'zip_code', 'specialization', 'room_number', 'prof_title', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Doctor.objects.filter(email=email).exists():
            raise forms.ValidationError('Podany adres e-mail jest już zajęty.')
        return email


class SecretaryRegistrationForm(UserCreationForm):
    employment_status = forms.ChoiceField(choices=Secretary.EMPLOYMENT_STATUS_CHOICES, initial='Aktywny')
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    phone_number = forms.CharField(max_length=15)
    city = forms.CharField(max_length=120)
    street = forms.CharField(max_length=120)
    house_number = forms.CharField(max_length=10)
    zip_code = forms.CharField(max_length=10)
    role = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('secretary', 'Secretary'), ('patient', 'Patient')],
                             initial='doctor', label='Role')

    class Meta(UserCreationForm.Meta):
        model = Secretary
        fields = ('email', 'password1', 'password2', 'employment_status', 'first_name', 'last_name', 'phone_number',
                  'city', 'street', 'house_number', 'zip_code','role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Secretary.objects.filter(email=email).exists():
            raise forms.ValidationError('Podany adres e-mail jest już zajęty.')
        return email


