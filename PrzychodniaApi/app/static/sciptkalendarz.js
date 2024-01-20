let currentWeekStartDate = new Date(); // Początkowa data aktualnego tygodnia

function formatHour(hour) {
    const hours = Math.floor(hour);
    const minutes = (hour - hours) * 60;
    return hours.toString().padStart(2, '0') + "-" + minutes.toString().padStart(2, '0');
}

function updateCalendarView(doctorId) {
    const dateString = currentWeekStartDate.toISOString().split('T')[0];
    const url = `/kalendarz/api/get_calendar_data/?date=${dateString}&doctor_id=${doctorId}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd sieci lub odpowiedź serwera');
            }
            return response.json();
        })
        .then(data => {
            updateCalendarSlots(data);
        })
        .catch(error => {
            console.error('Błąd przy pobieraniu danych kalendarza:', error);
        });
}

function updateCalendarSlots(data) {
    // Najpierw czyścimy wszystkie sloty
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('available', 'unavailable');
        slot.textContent = '';
    });

    // Następnie aktualizujemy sloty z nowymi danymi
    data.forEach(entry => {
        const slotId = `#slot-${entry.day}-${entry.time.replace(':', '-')}`;
        const slot = document.querySelector(slotId);

        if (slot) {
            slot.classList.add('available');
            slot.textContent = 'Dostępne';
        } else {
            console.error('Nie znaleziono slotu dla identyfikatora:', slotId);
        }
    });
}

// Funkcja do przewijania tygodni w bok
function changeWeek(direction) {
    currentWeekStartDate.setDate(currentWeekStartDate.getDate() + (direction * 7));
    updateHeaderDates();
    updateCalendarView(doctorId); // Aktualizacja kalendarza z wybranym lekarzem
}

function updateHeaderDates() {
    const weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];

    for (let i = 0; i < 5; i++) {
        const date = new Date(currentWeekStartDate);
        date.setDate(date.getDate() + i);
        const dateString = date.toISOString().split('T')[0];
        document.getElementById(`day-${i}`).textContent = `${weekdays[i]} (${dateString})`;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Początkowe pobranie kalendarza z wybranym lekarzem
    const doctorSelect = document.getElementById('doctorSelect');
    const initialSelectedDoctorId = doctorSelect.value;

    updateHeaderDates();
    updateCalendarView(initialSelectedDoctorId);

    // Obsługa przycisków do przewijania tygodni
    document.getElementById('prevWeekButton').addEventListener('click', function() {
        changeWeek(-1);
    });

    document.getElementById('nextWeekButton').addEventListener('click', function() {
        changeWeek(1);
    });
});
