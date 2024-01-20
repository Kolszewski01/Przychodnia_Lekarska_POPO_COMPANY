from django.urls import path
from .views import (generuj_daty_i_godziny, wyswietl_terminy, usun_wszystkie_wpisy, lista_lekarzy, widok_kalendarza,
                    get_calendar_data, create_reservation)

urlpatterns = [
    path('generuj_daty_i_godziny/', generuj_daty_i_godziny, name='generuj_daty_i_godziny'),
    path('wyswietl_daty_i_godziny/', wyswietl_terminy, name='wyswietl_daty_i_godziny'),
    path('kalendarz/usun_wszystkie_wpisy/', usun_wszystkie_wpisy, name='usun_wszystkie_wpisy'),
    path('lekarze/', lista_lekarzy, name='lista_lekarzy'),
    path('kalendarz-lekarza/<int:doctor_id>/', widok_kalendarza, name='nazwa_widoku_kalendarza'),
    path('api/get_calendar_data/', get_calendar_data, name='get_calendar_data'),
    path('create_reservation/', create_reservation, name='create_reservation'),

]
