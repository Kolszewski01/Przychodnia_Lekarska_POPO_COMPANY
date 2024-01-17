from time import timezone
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .models import Calendar, Reservation
from .forms import DateForm
import datetime
from rest_framework.response import Response
from .serializers import CalendarSerializer


def generuj_daty_i_godziny(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            end_date = form.cleaned_data['end_date']

            # Ustal datę początkową
            start_date = datetime.date.today()

            # Ustal interwał co pół godziny
            interval = datetime.timedelta(minutes=30)

            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() < 5:  # Sprawdź, czy to dzień od poniedziałku do piątku (0-4)
                    godzina = datetime.datetime.combine(current_date, datetime.time(8, 0))
                    godzina = timezone.make_aware(godzina)  # Poprawnie użyj make_aware
                    end_of_day = timezone.make_aware(
                        datetime.datetime.combine(current_date, datetime.time(17, 30)))  # Ostatnia godzina (17:30)
                    while godzina <= end_of_day:
                        nowy_rekord = Calendar(data=godzina)
                        nowy_rekord.save()
                        godzina += interval
                        if godzina.time() > datetime.time(17, 30):  # Zapobieganie tworzeniu godziny poza zakresem
                            break
                        godzina = timezone.make_aware(datetime.datetime.combine(current_date, godzina.time()))

                current_date += datetime.timedelta(days=1)

            return render(request, 'wyswietlanie_daty_i_godziny.html', {'daty_i_godziny': Calendar.objects.all()})
    else:
        form = DateForm()

    return render(request, 'formularz_daty.html', {'form': form})


def wyswietl_terminy(request):
    wszystkie_terminy = Calendar.objects.all()
    zarezerwowane_terminy = Reservation.objects.values_list('data', flat=True)

    dostepne_terminy = {}
    for termin in wszystkie_terminy:
        day = termin.data.weekday()
        time = termin.data.strftime('%H:%M')
        if termin.data not in zarezerwowane_terminy:
            if day not in dostepne_terminy:
                dostepne_terminy[day] = []
            dostepne_terminy[day].append(time)

    godziny = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30) if not (h == 17 and m == 30)]
    dni_tygodnia = range(5)

    return render(request, 'wyswietlanie_daty_i_godziny.html', {
        'dostepne_terminy': dostepne_terminy,
        'godziny': godziny,
        'dni_tygodnia': dni_tygodnia
    })


def usun_wszystkie_wpisy(request):
    if request.method == 'POST':
        # Usuń wszystkie wpisy z modelu Calendar
        Calendar.objects.all().delete()
        # Przekieruj z powrotem do strony głównej lub do innego widoku
        return redirect('generuj_daty_i_godziny')

class CalendarList(APIView):
    def get(self, request, format=None):
        calendars = Calendar.objects.all()
        serializer = CalendarSerializer(calendars, many=True)
        return Response(serializer.data)
