from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
import os

from django.views import View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import DoctorRegistrationForm, SecretaryRegistrationForm
from patient.models import Patient
from patient_record.models import PatientRecord

from patient_record.forms import PatientRecordForm


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

class MedicalRecordsView(View):
    template_name = 'medical_records.html'

    def get(self, request, *args, **kwargs):
        pesel = request.GET.get('pesel', '')
        patient = None
        medical_records = None

        if pesel:
            patient = get_object_or_404(Patient, pesel=pesel)
            medical_records = PatientRecord.objects.filter(patient=patient)

        return render(request, self.template_name, {'patient': patient, 'medical_records': medical_records, 'searched_pesel': pesel})

class EditMedicalRecordView(View):
    template_name = 'edit_medical_record.html'

    def get(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        record = get_object_or_404(PatientRecord, id=record_id)
        form = PatientRecordForm(instance=record)
        self.record = record
        return render(request, self.template_name, {'form': form, 'record': record})

    def post(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        record = get_object_or_404(PatientRecord, id=record_id)
        form = PatientRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            return redirect('medical_records')

        return render(request, self.template_name, {'form': form, 'record': record})