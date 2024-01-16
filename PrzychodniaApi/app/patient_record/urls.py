from django.urls import path
from .views import PatientRecordListView, PatientRecordAdminView

urlpatterns = [
    path('patient-records/', PatientRecordListView.as_view(), name='patient-record-list'),
    path('patient-records/admin/', PatientRecordAdminView.as_view(), name='patient-record-admin-list'),
    # path('prescriptions/', PrescriptionView.as_view(), name='prescription-list'),
    # path('prescriptions/<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),
]