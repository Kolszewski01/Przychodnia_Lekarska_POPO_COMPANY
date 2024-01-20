from django.urls import path
from .views import doctors_view, MedicalRecordsView, MedicalRecordDetailView

urlpatterns = [
    path('doctors/', doctors_view, name='doctors'),
    path('medical_records/', MedicalRecordsView.as_view(), name='medical_records'),
    path('medical_records/<int:patient_id>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
]