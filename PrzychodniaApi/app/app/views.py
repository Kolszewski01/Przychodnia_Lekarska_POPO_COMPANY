from django.shortcuts import render
from worker.models import Doctor, Secretary
from patient.models import Patient
from visit.models import Visit



def home(request):
    role = getattr(request.user, 'role', None) if request.user.is_authenticated else None
    num_doctors = Doctor.objects.count()
    num_secretaries = Secretary.objects.count()
    num_patients = Patient.objects.count()
    doctors = Doctor.objects.all()  # Pobieranie wszystkich lekarzy


    user_visits = None
    if request.user.is_authenticated and role == 'patient' and hasattr(request.user, 'patient'):
        user_visits = Visit.objects.filter(patient=request.user.patient)

    secretary_visits = None
    if request.user.is_authenticated and role == 'secretary':
        secretary_visits = Visit.objects.all()

    context = {
        'num_doctors': num_doctors,
        'num_secretaries': num_secretaries,
        'num_patients': num_patients,
        'role': role,
        'user_visits': user_visits,
        'secretary_visits': secretary_visits,  # Dodaj informacje o wizytach dla sekretarki
        'doctors': doctors,  # Dodanie lekarzy do kontekstu

    }

    return render(request, 'index.html', context)
