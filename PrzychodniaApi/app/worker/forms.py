from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, Secretary

class DoctorRegistrationForm(UserCreationForm):
    specialization = forms.CharField(max_length=120, label='Specialization')
    room_number = forms.CharField(max_length=10, label='Room Number')
    prof_title = forms.ChoiceField(choices=Doctor.PROF_TITLE_CHOICES, label='Professional Title', initial='Dr. med.')
    name = forms.CharField(max_length=120, label='Name')  # Dodaj to pole

    role = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('secretary', 'Secretary'), ('patient', 'Patient')],
                             label='Role', initial='doctor')

    email = forms.EmailField(max_length=254, label='Email', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    city = forms.CharField(max_length=120, label='City')
    street = forms.CharField(max_length=120, label='Street')
    house_number = forms.CharField(max_length=10, label='House Number')
    zip_code = forms.CharField(max_length=10, label='ZIP Code')
    visit_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0.0,
        label='Price for Visit'
    )

    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = (
        'name','email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'city', 'street', 'house_number',
        'zip_code', 'specialization', 'room_number', 'prof_title', 'role', 'visit_price')
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


