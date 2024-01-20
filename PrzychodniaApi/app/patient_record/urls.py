from django.urls import path
from .views import PatientRecordListView, PatientRecordAdminView,PatientPrescriptionsListView, PrescriptionAdminView

urlpatterns = [
    # path('patient-records/', PatientRecordListView.as_view(), name='patient-record-list'),
    path('patient-records/worker/', PatientRecordAdminView.as_view(), name='patient-record-admin-list'),
    path('prescriptions/', PatientPrescriptionsListView.as_view(), name='prescription-list'),
    path('prescriptions/worker/', PrescriptionAdminView.as_view(), name='prescription-record-admin-list'),
    path('patient_records/', PatientRecordListView.as_view(), name='patient_records_list'),
]