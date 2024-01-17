# google_calendar_integration/urls.py

from django.urls import path
from .views import google_login, oauth2callback, znajdz_dostepne_terminy, zarezerwuj_termin

urlpatterns = [
    path('google/login/', google_login, name='google_login'),
    path('google/oauth2callback/', oauth2callback, name='oauth2callback'),
    path('znajdz-terminy/', znajdz_dostepne_terminy, name='znajdz_terminy'),
    path('zarezerwuj-termin/', zarezerwuj_termin, name='zarezerwuj_termin'),
    # Możesz dodać więcej ścieżek, jeśli potrzebujesz
]
