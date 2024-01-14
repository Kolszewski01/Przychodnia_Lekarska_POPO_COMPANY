from django.db import models
from user.models import User
from worker.models import Doctor, Secretary

class Admin(User):
    def add_doctor(self, email, password, first_name, last_name, phone_number, city, street, house_number, zip_code, specialization, room_number, prof_title,employment_status, **extra_fields):

        doctor = Doctor(
            email=email, first_name=first_name, last_name=last_name,
            phone_number=phone_number, city=city, street=street,
            house_number=house_number, zip_code=zip_code,
            specialization=specialization, room_number=room_number,
            prof_title=prof_title,employment_status=employment_status, **extra_fields
        )
        doctor.set_password(password)
        doctor.save()
        return doctor

    def add_secretary(self, email, password, first_name, last_name, phone_number, city, street, house_number, zip_code, **extra_fields):

        secretary = Secretary(
            email=email, first_name=first_name, last_name=last_name,
            phone_number=phone_number, city=city, street=street,
            house_number=house_number, zip_code=zip_code,
            **extra_fields
        )
        secretary.set_password(password)
        secretary.save()
        return secretary

    def remove_worker(self, worker_id, worker_type):
        """
        Usuwa pracownika (lekarza lub sekretarkę) na podstawie ID.
        """
        if worker_type == 'doctor':
            model = Doctor
        elif worker_type == 'secretary':
            model = Secretary
        else:
            raise ValueError("Nieprawidłowy typ pracownika: 'doctor' lub 'secretary'")

        model.objects.filter(id=worker_id).delete()

    def modify_worker(self, worker_id, worker_type, **updated_fields):
        """
        Modyfikuje dane pracownika (lekarza lub sekretarki).
        """
        if worker_type == 'doctor':
            model = Doctor
        elif worker_type == 'secretary':
            model = Secretary
        else:
            raise ValueError("Nieprawidłowy typ pracownika: 'doctor' lub 'secretary'")

        worker = model.objects.get(id=worker_id)
        for field, value in updated_fields.items():
            setattr(worker, field, value)
        worker.save()
