from django.shortcuts import render
from worker.models import Doctor, Secretary
from patient.models import Patient
from visit.models import Visit



def home(request):
    role = getattr(request.user, 'role', None) if request.user.is_authenticated else None
    num_doctors = Doctor.objects.count()
    num_secretaries = Secretary.objects.count()
    num_patients = Patient.objects.count()
    doctors = Doctor.objects.all()

    user_visits = None
    secretary_visits = None
    doctor_visits = None

    if request.user.is_authenticated:
        if role == 'patient' and hasattr(request.user, 'patient'):
            user_visits = Visit.objects.filter(patient=request.user.patient)
        elif role == 'secretary':
            secretary_visits = Visit.objects.all()
        elif role == 'doctor' and hasattr(request.user, 'doctor'):
            # Dla lekarza, pobierz wizyty przypisane do tego lekarza
            doctor_visits = Visit.objects.filter(doctor=request.user.doctor)

    context = {
        'num_doctors': num_doctors,
        'num_secretaries': num_secretaries,
        'num_patients': num_patients,
        'role': role,
        'user_visits': user_visits,
        'secretary_visits': secretary_visits,
        'doctor_visits': doctor_visits,
        'doctors': doctors,
    }

    return render(request, 'index.html', context)