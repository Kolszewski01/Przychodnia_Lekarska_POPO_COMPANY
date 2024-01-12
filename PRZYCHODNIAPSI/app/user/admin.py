from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AppPermission

admin.site.register(CustomUser)
admin.site.register(UserAdmin)
admin.site.register(AppPermission)
