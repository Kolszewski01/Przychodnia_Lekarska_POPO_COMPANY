let currentWeekStartDate = new Date(); // Początkowa data aktualnego tygodnia

// Funkcja do zmiany tygodnia
function changeWeek(direction) {
    currentWeekStartDate.setDate(currentWeekStartDate.getDate() + (direction * 7));
    console.log("Nowa data początkowa tygodnia: ", currentWeekStartDate.toISOString().split('T')[0]);
    updateHeaderDates();
    updateCalendarView();
}

// Funkcja do aktualizacji dat w nagłówkach
function updateHeaderDates() {
    const weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];
    for (let i = 0; i < 5; i++) {
        const date = new Date(currentWeekStartDate);
        date.setDate(date.getDate() + i);
        const dateString = date.toISOString().split('T')[0];
        document.getElementById(`day-${i}`).textContent = `${weekdays[i]} (${dateString})`;
    }
}

// Funkcja do aktualizacji widoku kalendarza
function updateCalendarView() {
    const dateString = currentWeekStartDate.toISOString().split('T')[0];
    console.log("Wysyłam zapytanie do API z datą: ", dateString);
    const url = `/kalendarz/api/get_calendar_data?date=${dateString}`;

    fetch(url)
        .then(response => {
            console.log("Odpowiedź serwera: ", response);
            return response.json();
        })
        .then(data => {
            console.log("Dane otrzymane od serwera: ", data);
            updateCalendarSlots(data);
        })
        .catch(error => {
            console.error('Błąd przy pobieraniu danych kalendarza: ', error);
            console.error('Problem z URL: ', url);
        });
}

// Funkcja do aktualizacji slotów w kalendarzu
function updateCalendarSlots(data) {
    // Iteruj po dniach tygodnia
    for (let day = 0; day < 5; day++) {
        const dayEntries = data.filter(entry => entry.day === day);
        const dayColumn = document.querySelector(`#day-${day}`);
        const slots = dayColumn.querySelectorAll('.time-slot');

        // Aktualizacja slotów na podstawie danych z serwera
        slots.forEach(slot => {
            const slotTime = slot.getAttribute('data-hour');
            if (dayEntries.some(entry => entry.time === slotTime)) {
                slot.classList.remove('unavailable');
                slot.classList.add('available');
                slot.textContent = 'Dostępne';
            } else {
                slot.classList.remove('available');
                slot.classList.add('unavailable');
                slot.textContent = 'Niedostępne';
            }
        });
    }
}

// Funkcja do dodawania nasłuchiwaczy do przycisków
function addListeners() {
    document.getElementById('prevWeekButton').addEventListener('click', function() {
        changeWeek(-1);
    });

    document.getElementById('nextWeekButton').addEventListener('click', function() {
        changeWeek(1);
    });
}

// Upewnij się, że daty są aktualizowane podczas inicjalizacji
document.addEventListener('DOMContentLoaded', function() {
    addListeners();
    updateHeaderDates();
});
v