from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Patient, PatientRecord, Prescription
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


# class PatientRecordListView(generics.ListAPIView):
#     serializer_class = PatientRecordSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return PatientRecord.objects.filter(patient=self.request.user.patient)
#
#     def list(self, request, *args, **kwargs):
#         patient_records = self.get_queryset()
#         return render(request, 'index.html', {'patient_records': patient_records})
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

class PrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]  # Make sure the user is authenticated

    def get_queryset(self):
        # Return only prescriptions related to the logged-in patient
        return Prescription.objects.filter(patient_record__patient=self.request.user.patient)


class PrescriptionAdminView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        # Zwróć wszystkie rekordy dla workera
        return Prescription.objects.all()

    def perform_create(self, serializer):
        # Przypisz pacjenta do nowego rekordu na podstawie relacji z PatientRecord
        serializer.save(patient_record__patient=self.request.user.patient)
