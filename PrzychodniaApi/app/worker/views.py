from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
import os
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import DoctorRegistrationForm, SecretaryRegistrationForm


def doctors_view(request):
    image_folder = 'static/images/profile_images'
    image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]

    return render(request, 'index.html', {'doctor_images': image_paths})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pomyślnie zarejestrowano lekarza.')
            return redirect('home')
        else:
            messages.error(request, 'Wystąpił błąd w formularzu. Spróbuj ponownie.')
    else:
        form = DoctorRegistrationForm()

    return render(request, 'admin_registration.html', {'form': form})

def register_secretary(request):
    if request.method == 'POST':
        form = SecretaryRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pomyślnie zarejestrowano sekretarkę.')
            return redirect('home')
        else:
            messages.error(request, 'Wystąpił błąd w formularzu. Spróbuj ponownie.')
    else:
        form = SecretaryRegistrationForm()

    return render(request, 'register_secretary.html', {'form': form})
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeView.as_view()(request)
        if form.status_code == 302:  # 302 to kod odpowiedzi przekierowania
            messages.success(request, 'Pomyślnie zmieniono hasło.')
            return redirect('home')  # Przekieruj do widoku home po pomyślnej zmianie hasła
    else:
        form = PasswordChangeView.as_view()(request)

    return render(request, 'change_password.html', {'form': form.context_data['form']})