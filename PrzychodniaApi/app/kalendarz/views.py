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
from visit.models import Visit
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
from django.db.models.functions import TruncDate, TruncTime
import json



@login_required
@csrf_exempt
def create_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            reservation_datetime = parse_datetime(data.get('data'))
            doctor_id = data.get('doctor_id')

            if reservation_datetime and is_naive(reservation_datetime):
                reservation_datetime = make_aware(reservation_datetime)

            # Get the doctor object
            doctor = get_object_or_404(Doctor, pk=doctor_id)

            # Use attributes from the doctor object
            room_number = doctor.room_number  # Assume that room_number is an attribute of Doctor
            visit_price = doctor.visit_price  # Assume that visit_price is an attribute of Doctor

            # Create the reservation
            reservation = Reservation.objects.create(
                data=reservation_datetime,
                patient=request.user.patient,
                doctor=doctor
            )

            # Create the associated visit
            visit = Visit.objects.create(
                reservation_copy=reservation,
                doctor=doctor,
                patient=request.user.patient,
                room_number=room_number,  # Set the room number from Doctor object
                price=visit_price  # Set the visit price from Doctor object
            )

            return JsonResponse({'status': 'success', 'visit_id': visit.id})
        except KeyError as e:
            # Return specific error message for missing data
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            # Handle any other exception
            return JsonResponse({'status': 'error', 'message': 'Unexpected error occurred'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def generuj_daty_i_godziny(request):
    doctors = Doctor.objects.all()  # Lista lekarzy

    if request.method == 'POST':
        if 'generate' in request.POST:
            form = DateForm(request.POST)
            if form.is_valid():
                end_date = form.cleaned_data['end_date']
                doctor_id = request.POST.get('doctor')
                doctor = get_object_or_404(Doctor, pk=doctor_id)

                start_date_time = timezone.localtime(timezone.now())  # Bieżąca data i godzina
                interval = timedelta(minutes=30)

                current_date = start_date_time.date()
                while current_date <= end_date:
                    start_time = time(8, 0)
                    end_time = time(17, 30) if current_date != start_date_time.date() else time(17, 0)

                    godzina = timezone.make_aware(datetime.combine(current_date, start_time))

                    while godzina.time() <= end_time:
                        if not Calendar.objects.filter(data=godzina, doctor=doctor).exists():
                            Calendar.objects.create(data=godzina, doctor=doctor)
                        godzina += interval
                        godzina = timezone.make_aware(datetime.combine(current_date, godzina.time()))

                    current_date += timedelta(days=1)

        elif 'delete' in request.POST:
            doctor_id = request.POST.get('delete_doctor')
            Calendar.objects.filter(doctor_id=doctor_id).delete()

        elif 'add_single' in request.POST:
            doctor_id = request.POST.get('doctor_single')
            data = request.POST.get('data_single')  # Format 'YYYY-MM-DD HH:MM'
            doctor = get_object_or_404(Doctor, pk=doctor_id)
            data_godzina = timezone.make_aware(datetime.fromisoformat(data))

            if not Calendar.objects.filter(data=data_godzina, doctor=doctor).exists():
                Calendar.objects.create(data=data_godzina, doctor=doctor)

        elif 'delete_single' in request.POST:
            appointment_id = request.POST.get('appointment_id')
            Calendar.objects.filter(id=appointment_id).delete()

        return redirect('generuj_daty_i_godziny')  # Nazwa widoku

    else:
        form = DateForm()

    appointments = Calendar.objects.all()
    return render(request, 'formularz_daty.html', {'form': form, 'doctors': doctors, 'appointments': appointments})
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

    zarezerwowane_terminy_set = set()
    zarezerwowane_terminy_qs = Reservation.objects.filter(doctor=doctor)
    for termin in zarezerwowane_terminy_qs:
        day = termin.data.weekday()
        data_czas_str = termin.data.strftime('%Y-%m-%d %H:%M')
        zarezerwowane_terminy_set.add((day, data_czas_str))

    terminy_kalendarza_qs = Calendar.objects.filter(doctor=doctor)
    terminy_kalendarza_set = set()
    for termin in terminy_kalendarza_qs:
        day = termin.data.weekday()
        data_czas_str = termin.data.strftime('%Y-%m-%d %H:%M')
        terminy_kalendarza_set.add((day, data_czas_str))

    dostepne_terminy_frontend = []
    for day, data_czas_str in terminy_kalendarza_set:
        if (day, data_czas_str) not in zarezerwowane_terminy_set:
            czas_str = data_czas_str[-5:].replace(':', '-')
            dostepne_terminy_frontend.append({"day": day, "time": czas_str})

    godziny = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30) if not (h == 17 and m == 30)]
    dni_tygodnia = range(5)

    return render(request, 'widok_kalendarza.html', {
        'doctor': doctor,
        'dostepne_terminy': dostepne_terminy_frontend,  # Przekazanie przetworzonych danych
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
        given_date = datetime.strptime(date_str, '%Y-%m-%d')
        given_date = timezone.make_aware(given_date)

        # Ustalanie poniedziałku i piątku tygodnia zawierającego podaną datę
        start_of_week = given_date - timedelta(days=given_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        print(start_of_week, end_of_week)
        print(end_of_week)

    except ValueError:

        return HttpResponseBadRequest('Niepoprawny format daty')

    doctor = get_object_or_404(Doctor, pk=doctor_id)
    reserved_slots = Reservation.objects.filter(doctor=doctor).values_list('data', flat=True)
    calendar_entries = Calendar.objects.filter(data__range=[start_of_week, end_of_week], doctor=doctor)
    now = timezone.now()
    # Dodajemy 1 godzinę do bieżącej godziny
    now_plus_one_hour = now + timedelta(hours=1)

    current_time_rounded = time(now_plus_one_hour.hour, now_plus_one_hour.minute)
    print(current_time_rounded)
    print(now_plus_one_hour)

    data = [
        {
            'day': entry.data.weekday(),
            'time': entry.data.strftime('%H-%M'),
            'reserved': entry.data in reserved_slots
        }
        for entry in calendar_entries
        if entry.data.weekday() < 5 and entry.data not in reserved_slots and
           (entry.data.date() > now_plus_one_hour.date() or
            (entry.data.date() == now_plus_one_hour.date() and time(entry.data.hour,
                                                                    entry.data.minute) > current_time_rounded))
    ]

    return JsonResponse(data, safe=False)


def reserved_appointments(request):
    # Pobierz wszystkie rezerwacje i dołącz powiązane obiekty lekarza i pacjenta
    appointments = Reservation.objects.select_related('doctor', 'patient').all()
    # Przygotuj dane do wyświetlenia w kalendarzu
    calendar_data = []
    for appointment in appointments:
        day = appointment.data.weekday()  # Dzień tygodnia jako liczba
        hour = appointment.data.strftime('%H:%M')  # Godzina jako tekst
        calendar_data.append({
            'day': day,
            'hour': hour,
            'doctor_name': f'{appointment.doctor.first_name} {appointment.doctor.last_name}',
            'patient_name': f'{appointment.patient.name} {appointment.patient.last_name}'
        })
    return render(request, 'secretary_calendar.html', {'calendar_data': calendar_data})


def usun_przeterminowane_rezerwacje():
    # Pobranie aktualnej daty i czasu
    print('USUN przeterminowane')

    teraz = timezone.now()

    # Usunięcie rezerwacji, które już minęły
    Reservation.objects.filter(data__lt=teraz).delete()

    # Usunięcie wpisów z kalendarza, które już minęły
    Calendar.objects.filter(data__lt=teraz).delete()