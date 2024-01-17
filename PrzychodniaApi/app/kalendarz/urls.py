from django.urls import path
from .views import generuj_daty_i_godziny, wyswietl_terminy, usun_wszystkie_wpisy

urlpatterns = [
    path('generuj_daty_i_godziny/', generuj_daty_i_godziny, name='generuj_daty_i_godziny'),
    path('wyswietl_daty_i_godziny/', wyswietl_terminy, name='wyswietl_daty_i_godziny'),
    path('kalendarz/usun_wszystkie_wpisy/', usun_wszystkie_wpisy, name='usun_wszystkie_wpisy'),

]
