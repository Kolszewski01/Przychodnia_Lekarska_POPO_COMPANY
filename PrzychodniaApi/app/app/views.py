from django.shortcuts import render

from worker.models import Doctor, Secretary
from patient.models import Patient

def home(request):
    role = getattr(request.user, 'role', None) if request.user.is_authenticated else None
    num_doctors = Doctor.objects.count()
    num_secretaries = Secretary.objects.count()
    num_patients = Patient.objects.count()

    context = {
        'num_doctors': num_doctors,
        'num_secretaries': num_secretaries,
        'num_patients': num_patients,
        'role': role,
    }

    return render(request, 'index.html', context)


