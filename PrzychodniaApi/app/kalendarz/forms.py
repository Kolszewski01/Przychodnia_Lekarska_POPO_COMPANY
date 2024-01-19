from django import forms

class DateForm(forms.Form):
    end_date = forms.DateField(
        input_formats=['%m/%d/%Y'],  # Ustawienie formatu daty na MM/DD/YYYY
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/DD/YYYY'  # Podpowiedź formatu w polu formularza
        })
    )
