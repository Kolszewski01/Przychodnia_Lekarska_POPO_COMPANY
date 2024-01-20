"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include
from .views import home
from patient.views import register_patient
from user.views import CustomLogoutView, CustomLoginView
from worker.views import register_doctor, register_secretary, change_password, MedicalRecordsView, EditMedicalRecordView
from patient_record.views import PrescriptionCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', home, name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register_patient/', register_patient, name='register_patient'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('kalendarz/', include('kalendarz.urls')),
    path('api/', include('patient_record.urls'), name='patient_record'),
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('register/secretary/', register_secretary, name='register_secretary'),
    path('change_password/', change_password, name='change_password'),
    path('prescription/create/', PrescriptionCreateView.as_view(), name='prescription_create'),
    path('medical_records/', MedicalRecordsView.as_view(), name='medical_records'),
    path('edit_medical_record/<int:record_id>/', EditMedicalRecordView.as_view(), name='edit_medical_record'),
]
