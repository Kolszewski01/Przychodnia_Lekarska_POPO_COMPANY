let currentWeekStartDate = new Date(); // Początkowa data aktualnego tygodnia

// Funkcja do zmiany tygodnia
function changeWeek(direction) {
    currentWeekStartDate.setDate(currentWeekStartDate.getDate() + (direction * 7));
    console.log("Nowa data początkowa tygodnia: ", currentWeekStartDate.toISOString().split('T')[0]);
    updateCalendarView();
}

// Funkcja do aktualizacji widoku kalendarza
function updateCalendarView() {
    const url = `/api/get_calendar_data?date=${currentWeekStartDate.toISOString().split('T')[0]}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateCalendarSlots(data);
        })
        .catch(error => console.error('Błąd przy pobieraniu danych kalendarza: ', error));
}

// Funkcja do aktualizacji slotów w kalendarzu
function updateCalendarSlots(data) {
    // Usunięcie istniejących slotów
    document.querySelectorAll('.time-slot').forEach(slot => slot.remove());

    // Dodanie nowych slotów zgodnie z otrzymanymi danymi
    data.forEach(entry => {
        const dayColumn = document.querySelector(`#day-${entry.day}`);
        if(dayColumn) {
            entry.times.forEach(time => {
                const slot = document.createElement('button');
                slot.className = 'time-slot available';
                slot.textContent = time;
                dayColumn.appendChild(slot);
            });
        }
    });
}

// Funkcja do dodawania nasłuchiwaczy do przycisków
function addListeners() {
    // Attaching event listener to 'previous week' button
    document.getElementById('prevWeekButton').addEventListener('click', function() {
        changeWeek(-1);
    });

    // Attaching event listener to 'next week' button
    document.getElementById('nextWeekButton').addEventListener('click', function() {
        changeWeek(1);
    });
}

// Ensure event listeners are added after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', addListeners);

// Dodanie nasłuchiwaczy po załadowaniu DOM
document.addEventListener('DOMContentLoaded', addListeners);
