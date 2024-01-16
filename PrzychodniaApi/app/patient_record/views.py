from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Patient, PatientRecord
from .serializers import PatientRecordSerializer

from rest_framework import permissions

class IsPatientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Sprawdź, czy żądający użytkownik jest właścicielem pacjenta
        return obj.user == request.user

class PatientRecordListView(generics.ListCreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated]  # Upewnij się, że użytkownik jest zalogowany

    def get_queryset(self):
        # Zwróć tylko rekordy dotyczące zalogowanego pacjenta
        return PatientRecord.objects.filter(patient=self.request.user.patient)

    def perform_create(self, serializer):
        # Przypisz pacjenta do nowego rekordu
        serializer.save(patient=self.request.user.patient)

class PatientRecordAdminView(generics.ListCreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Upewnij się, że użytkownik jest zalogowany i to administrator

    def get_queryset(self):
        # Zwróć wszystkie rekordy dla administratora
        return PatientRecord.objects.all()

    def perform_create(self, serializer):
        # Przypisz pacjenta do nowego rekordu
        serializer.save(patient=self.request.user.patient)
