let currentWeekStartDate = new Date(); // Początkowa data aktualnego tygodnia

// Funkcja do zmiany tygodnia
function changeWeek(direction) {
    currentWeekStartDate.setDate(currentWeekStartDate.getDate() + (direction * 7));
    console.log("Nowa data początkowa tygodnia: ", currentWeekStartDate.toISOString().split('T')[0]);
    updateHeaderDates();
    updateCalendarView();  // Aktualizacja widoku kalendarza z nowymi danymi
}

// Funkcja do aktualizacji dat w nagłówkach
function updateHeaderDates() {
    const weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];

    // Cofnięcie daty o 3 dni
    const startDate = new Date(currentWeekStartDate);
    startDate.setDate(startDate.getDate() - 3);

    for (let i = 0; i < 5; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);
        const dateString = date.toISOString().split('T')[0];
        document.getElementById(`day-${i}`).textContent = `${weekdays[i]} (${dateString})`;
    }
}

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
        });
}

function updateCalendarSlots(data) {
    // Czyszczenie poprzednich stanów slotów
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('available', 'unavailable');
        slot.textContent = 'Ładowanie...';
    });

    // Iteruj po dniach tygodnia
    for (let day = 0; day < 5; day++) {
        const dayEntries = data.filter(entry => entry.day === day);
        for (let hour = 8; hour <= 17; hour += 0.5) {
            // Zamiana dwukropka na myślnik w identyfikatorze
            let hourString = hour.toString().padStart(2, '0') + ":00";
            hourString = hourString.replace(":", "-");

            const slotId = `#slot-${day}-${hourString}`;
            const slot = document.querySelector(slotId);
            if (!slot) {
                console.error('Nie znaleziono slotu dla identyfikatora: ', slotId);
                continue;
            }

            if (dayEntries.some(entry => entry.time === hourString.replace("-", ":"))) {
                slot.classList.add('available');
                slot.textContent = 'Dostępne';
            } else {
                slot.classList.add('unavailable');
                slot.textContent = 'Niedostępne';
            }
        }
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
