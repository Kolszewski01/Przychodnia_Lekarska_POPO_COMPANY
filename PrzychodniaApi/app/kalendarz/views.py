from time import timezone
from datetime import datetime, timedelta, date, time
from django.db.models import ExpressionWrapper, F
from django.forms import DateTimeField
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Calendar, Reservation
from .forms import DateForm
from rest_framework.response import Response
from .serializers import CalendarSerializer
from worker.models import Doctor
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware, is_naive
from django.utils.dateparse import parse_datetime
import json



@login_required
@csrf_exempt
def create_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            reservation_datetime = parse_datetime(data.get('data'))

            if reservation_datetime and is_naive(reservation_datetime):
                reservation_datetime = make_aware(reservation_datetime)

            # Cofnięcie rezerwacji o 3 dni
            adjusted_reservation_datetime = reservation_datetime + timedelta(days=4)

            reservation = Reservation.objects.create(
                data=adjusted_reservation_datetime,
                patient=request.user.patient
            )
            return JsonResponse({'status': 'success'})
        except KeyError:
            return JsonResponse({'status': 'error'}, status=400)

    return JsonResponse({'status': 'error'}, status=405)

def generuj_daty_i_godziny(request):
    doctors = Doctor.objects.all()  # Dodaj listę lekarzy do kontekstu

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            end_date = form.cleaned_data['end_date']
            doctor_id = request.POST.get('doctor')  # Pobierz ID lekarza z formularza
            doctor = get_object_or_404(Doctor, pk=doctor_id)  # Pobierz obiekt lekarza

            # Ustal datę początkową
            start_date = date.today()

            # Ustal interwał co pół godziny
            interval = timedelta(minutes=30)

            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() < 5:  # Sprawdź, czy to dzień od poniedziałku do piątku (0-4)
                    godzina = datetime.combine(current_date, time(8, 0))
                    godzina = timezone.make_aware(godzina)  # Poprawnie użyj make_aware
                    end_of_day = timezone.make_aware(datetime.combine(current_date, time(17, 30)))  # Ostatnia godzina (17:30)

                    while godzina <= end_of_day:
                        nowy_rekord = Calendar(data=godzina, doctor=doctor)
                        nowy_rekord.save()
                        godzina += interval
                        if godzina.time() > time(17, 30):  # Zapobieganie tworzeniu godziny poza zakresem
                            break
                        godzina = timezone.make_aware(datetime.combine(current_date, godzina.time()))

                current_date += timedelta(days=1)

            # Przekierowanie po utworzeniu terminów
            return redirect('generuj_daty_i_godziny')  # Zmień na odpowiednią nazwę widoku

    else:
        form = DateForm()

    return render(request, 'formularz_daty.html', {'form': form, 'doctors': doctors})


def wyswietl_terminy(request):
    wszystkie_terminy = Calendar.objects.all()
    zarezerwowane_terminy = Reservation.objects.annotate(
        datetime_field=ExpressionWrapper(
            F('data'),
            output_field=DateTimeField()
        )
    ).values_list('datetime_field', flat=True)

    dostepne_terminy = []

    for termin in wszystkie_terminy:
        if termin.data not in zarezerwowane_terminy:
            dostepne_terminy.append(termin)

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
        'dni_tygodnia': dni_tygodnia,
        'doctor_id': doctor_id,
    })


@require_GET
def get_calendar_data(request):
    date_str = request.GET.get('date')
    doctor_id = request.GET.get('doctor_id', request.session.get('selected_doctor_id', None))

    if not date_str or not doctor_id:
        return JsonResponse({'error': 'Brak daty lub ID lekarza w zapytaniu GET'}, status=400)

    try:
        start_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        aware_start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        aware_end_date = timezone.make_aware(datetime.combine(start_date + timedelta(days=4), datetime.max.time()))
    except ValueError:
        return HttpResponseBadRequest('Niepoprawny format daty')

    # Pobranie obiektu lekarza
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    # Zapisanie wybranego lekarza w sesji
    request.session['selected_doctor_id'] = doctor_id

    # Filtrowanie wpisów kalendarza według lekarza i daty
    calendar_entries = Calendar.objects.filter(data__range=[aware_start_date, aware_end_date], doctor=doctor)
    data = [
        {
            'day': entry.data.weekday(),
            'time': entry.data.strftime('%H-%M')  # Format 'HH-MM'
        }
        for entry in calendar_entries
    ]

    return JsonResponse(data, safe=False)
