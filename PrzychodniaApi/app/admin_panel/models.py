# from django.db import models
# from user.models import User
# from worker.models import Doctor, Secretary
# from django.db import models
#
# class Admin(User):
#     def add_doctor(self, first_name, last_name, specialization, room_number, phone_number):
#         doctor = Doctor(
#             first_name=first_name,
#             last_name=last_name,
#             specialization=specialization,
#             room_number=room_number,
#             phone_number=phone_number
#         )
#         doctor.save()
#
#     def add_secretary(self, first_name, last_name, role, working_hours, office_phone):
#         secretary = Secretary(
#             first_name=first_name,
#             last_name=last_name,
#             role=role,
#             working_hours=working_hours,
#             office_phone=office_phone
#         )
#         secretary.save()
#
