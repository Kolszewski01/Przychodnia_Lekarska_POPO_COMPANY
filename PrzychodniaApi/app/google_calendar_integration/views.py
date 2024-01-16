# google_calendar_integration/views.py

from django.shortcuts import redirect, render
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
from django.conf import settings
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError


def google_login(request):
    # Ścieżka do pliku JSON z danymi uwierzytelniającymi
    client_secrets_file = os.path.join(settings.BASE_DIR, 'templates/google/affable-heading-411407-935acd233189.json')

    # Przepływ OAuth
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://localhost:8000/google_calendar/oauth2callback'
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # Zapisz 'state' w sesji
    request.session['state'] = state

    return redirect(authorization_url)

def oauth2callback(request):
    # Pobierz 'state' z sesji
    state = request.session['state']

    client_secrets_file = os.path.join(settings.BASE_DIR, 'templates/google/affable-heading-411407-935acd233189.json')

    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=['https://www.googleapis.com/auth/calendar'],
        state=state,
        redirect_uri='http://localhost:8000/google_calendar/oauth2callback'
    )

    flow.fetch_token(authorization_response=request.get_full_path())

    credentials = flow.credentials

    # Zapisz dane uwierzytelniające w sesji
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect('ścieżka/do/widoku/obsługującego/sukces')

def wykonaj_zadanie_z_google_calendar(request):
    # Pobierz dane uwierzytelniające z sesji
    credentials_data = request.session.get('credentials', {})

    # Stwórz obiekt Credentials
    credentials = Credentials(**credentials_data)

    # Połącz się z Google Calendar API
    service = build('calendar', 'v3', credentials=credentials)

    # Wykonaj żądanie, np. pobierz wydarzenia z kalendarza
    events_result = service.events().list(calendarId='primary').execute()


def znajdz_dostepne_terminy(request, start_date, end_date):
    credentials_data = request.session.get('credentials', {})
    credentials = Credentials(**credentials_data)

    service = build('calendar', 'v3', credentials=credentials)

    # Zakładając, że masz już zakres dat (start_date i end_date)
    # w których szukasz dostępnych terminów
    result = service.freebusy().query(body={
        "timeMin": start_date,
        "timeMax": end_date,
        "items": [{"id": 'primary'}]  # Można dostosować do konkretnego ID kalendarza
    }).execute()

    # Przetwarzanie wyniku, aby znaleźć dostępne sloty czasowe
    # ...
    busy_times = result['calendars']['primary']['busy']

    dostepne_terminy = []
    ostatni_koniec = datetime.fromisoformat(start_date)

    for busy in busy_times:
        busy_start = datetime.fromisoformat(busy['start'])
        busy_end = datetime.fromisoformat(busy['end'])

        if busy_start > ostatni_koniec:
            # Znaleziono wolny slot
            dostepne_terminy.append({'start': ostatni_koniec, 'end': busy_start})

        ostatni_koniec = busy_end

    # Sprawdź, czy jest wolny czas między ostatnim zajętym slotem a end_date
    if ostatni_koniec < datetime.fromisoformat(end_date):
        dostepne_terminy.append({'start': ostatni_koniec, 'end': datetime.fromisoformat(end_date)})

    return dostepne_terminy


def zarezerwuj_termin(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        credentials_data = request.session.get('credentials', {})
        credentials = Credentials(**credentials_data)

        service = build('calendar', 'v3', credentials=credentials)

        event = {
            'summary': 'Rezerwacja wizyty',
            'start': {'dateTime': start_time},
            'end': {'dateTime': end_time},
        }

        try:
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            return render(request, 'potwierdzenie.html', {'event': created_event})
        except HttpError as error:
            return render(request, 'blad.html', {'error': f'Wystąpił błąd: {error}'})
    else:
        # Przykładowy szablon z formularzem do rezerwacji terminu
        return render(request, 'formularz_rezerwacji.html')