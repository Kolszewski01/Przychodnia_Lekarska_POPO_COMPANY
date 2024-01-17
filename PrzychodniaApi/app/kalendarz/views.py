from time import timezone

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Calendar, Reservation
from .forms import DateForm
import datetime
from rest_framework.response import Response
from .serializers import CalendarSerializer
from worker.models import Doctor
from django.utils.dateparse import parse_date



def generuj_daty_i_godziny(request):
    doctors = Doctor.objects.all()  # Dodaj listę lekarzy do kontekstu

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            end_date = form.cleaned_data['end_date']
            doctor_id = request.POST.get('doctor')  # Pobierz ID lekarza z formularza
            doctor = get_object_or_404(Doctor, pk=doctor_id)  # Pobierz obiekt lekarza

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
                        nowy_rekord = Calendar(data=godzina, doctor=doctor)
                        nowy_rekord.save()
                        godzina += interval
                        if godzina.time() > datetime.time(17, 30):  # Zapobieganie tworzeniu godziny poza zakresem
                            break
                        godzina = timezone.make_aware(datetime.datetime.combine(current_date, godzina.time()))

                current_date += datetime.timedelta(days=1)

            # Przekierowanie po utworzeniu terminów
            return redirect('generuj_daty_i_godziny')  # Zmień na odpowiednią nazwę widoku

    else:
        form = DateForm()

    return render(request, 'formularz_daty.html', {'form': form, 'doctors': doctors})


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


def lista_lekarzy(request):
    doctors = Doctor.objects.all()
    return render(request, 'lista_lekarzy.html', {'doctors': doctors})



def widok_kalendarza(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    terminy = Calendar.objects.filter(doctor=doctor)

    # Stworzenie struktury danych dla dostępnych terminów
    dostepne_terminy = {day: [] for day in range(5)}  # Dni od poniedziałku (0) do piątku (4)
    for termin in terminy:
        day = termin.data.weekday()
        time = termin.data.strftime('%H:%M')
        if day in dostepne_terminy:
            dostepne_terminy[day].append(time)

    godziny = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30) if not (h == 17 and m == 30)]
    dni_tygodnia = range(5)

    return render(request, 'widok_kalendarza.html', {
        'doctor': doctor,
        'dostepne_terminy': dostepne_terminy,
        'godziny': godziny,
        'dni_tygodnia': dni_tygodnia
    })


def get_calendar_data(request):
    # Pobierz datę z zapytania GET
    date_str = request.GET.get('date')
    if date_str:
        start_date = parse_date(date_str)
        if start_date:
            # Ustaw zakres daty na cały tydzień
            end_date = start_date + datetime.timedelta(days=6)

            # Pobierz dane z modelu Calendar
            calendar_entries = Calendar.objects.filter(data__range=[start_date, end_date])

            # Przygotuj dane do odpowiedzi
            data = [{'day': entry.data.weekday(), 'time': entry.data.strftime('%H:%M')} for entry in calendar_entries]
            return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Niepoprawna data'}, status=400)