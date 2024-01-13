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
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView


from .views import home
from user.views import register_view, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wizyta/', include(('wizyta.urls', 'wizyta'), namespace="wizyta")),
    path('pracownik/', include(('pracownik.urls', 'pracownik'), namespace="pracownik")),
    path('register/', register_view, name='register'),
    path('dokumentacja_medyczna/', include(('dokumentacja_medyczna.urls', 'dokumentacja_medyczna'), namespace="dokumentacja_medyczna")),
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

