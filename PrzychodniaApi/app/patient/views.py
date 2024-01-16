from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientRegistrationForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pomyślnie zarejestrowano pacjenta.')
            return redirect('home')
        else:
            messages.error(request, 'Wystąpił błąd w formularzu. Spróbuj ponownie.')
    else:
        form = PatientRegistrationForm()

    return render(request, 'register_patient.html', {'form': form})