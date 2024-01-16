from django.urls import path
from .views import PatientRecordListView, PatientRecordAdminView, PrescriptionListView, PrescriptionAdminView

urlpatterns = [
    path('patient-records/', PatientRecordListView.as_view(), name='patient-record-list'),
    path('patient-records/worker/', PatientRecordAdminView.as_view(), name='patient-record-admin-list'),
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/worker/', PrescriptionAdminView.as_view(), name='prescription-record-admin-list'),
]