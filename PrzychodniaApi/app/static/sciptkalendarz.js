
function changeWeek(direction) {
    // Tutaj logika zmiany tygodnia
    // 'direction' może być -1 dla poprzedniego tygodnia lub 1 dla następnego
    console.log("Zmiana tygodnia na: ", direction);
}

// Dodanie obsługi zdarzeń do slotów czasowych
document.querySelectorAll('.time-slot').forEach(slot => {
    slot.addEventListener('click', () => {
        const hour = slot.getAttribute('data-hour');
        const day = slot.getAttribute('data-day');
        console.log("Wybrano slot: ", day, hour);
        // Tutaj można dodać logikę rezerwacji lub wyświetlenia szczegółów
    });
});