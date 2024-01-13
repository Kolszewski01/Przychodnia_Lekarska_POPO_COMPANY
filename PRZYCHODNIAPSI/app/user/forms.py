from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =('pesel', 'imie', 'drugie_imie', 'nazwisko',
                                                 'nr_telefonu', 'miejscowosc', 'ulica',
                                                 'nr_domu', 'kod_pocztowy')

        def save(self, commit=True):
            user = super().save(commit=False)
            user.username = user.pesel  # Ustaw pesel jako username
            if commit:
                user.save()
            return user

class CustomAuthenticationForm(AuthenticationForm):
    pesel = forms.CharField(max_length=11, label='PESEL', widget=forms.TextInput(attrs={'autofocus': True}))

    class Meta:
        model = CustomUser
        fields = ['pesel', 'password']

