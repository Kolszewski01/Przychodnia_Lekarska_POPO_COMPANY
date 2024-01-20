from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from patient.models import Patient
from .forms import PrescriptionForm
from .models import PatientRecord, Prescription
from .serializers import PatientRecordSerializer, PrescriptionSerializer
from django.views.generic import ListView
from rest_framework import permissions

class IsPatientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Sprawdź, czy żądający użytkownik jest właścicielem pacjenta
        return obj.user == request.user

class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        # Sprawdź, czy użytkownik ma rolę worker
        return request.user.is_worker

class PatientRecordListView(ListView):
    model = PatientRecord
    template_name = 'patient_records_list.html'
    context_object_name = 'patient_records'

    def get_queryset(self):
        return PatientRecord.objects.filter(patient=self.request.user.patient)

class PatientRecordAdminView(generics.ListCreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated, IsWorker]  # Upewnij się, że użytkownik jest zalogowany i to administrator

    def get_queryset(self):
        # Zwróć wszystkie rekordy dla administratora
        return PatientRecord.objects.all()

    def perform_create(self, serializer):
        # Przypisz pacjenta do nowego rekordu
        serializer.save(patient=self.request.user.patient)

class PatientPrescriptionsListView(ListView):
    model = Prescription
    template_name = 'patient_prescriptions_list.html'
    context_object_name = 'prescriptions'
    ordering = ['-prescribed_date']

    def get_queryset(self):
        return Prescription.objects.filter(patient_record__patient=self.request.user.patient)


class PrescriptionCreateView(View):
    template_name = 'prescription_create.html'

    def get(self, request, *args, **kwargs):
        form = PrescriptionForm()
        return render(request, self.template_name, {'form': form, 'success_message': None})

    def post(self, request, *args, **kwargs):
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()

            success_message = 'Pomyślnie dodano receptę!'
            return render(request, self.template_name, {'form': PrescriptionForm(), 'success_message': success_message})

        return render(request, self.template_name, {'form': form, 'success_message': None})
class PrescriptionAdminView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        # Zwróć wszystkie rekordy dla workera
        return Prescription.objects.all()

    def perform_create(self, serializer):
        # Przypisz pacjenta do nowego rekordu na podstawie relacji z PatientRecord
        serializer.save(patient_record__patient=self.request.user.patient)

