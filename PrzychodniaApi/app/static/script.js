document.addEventListener('DOMContentLoaded', function() {
    var myButton = document.getElementById('logout-form');

    if (myButton) {
        myButton.addEventListener('click', function() {
            showAlert();
        });
    }

    function showAlert() {
        alert('Wylogowano pomyślnie!');
    }
});

// Funkcja do zwiększania czcionki
    function increaseFontSize() {
      const currentSize = parseFloat(window.getComputedStyle(document.documentElement).getPropertyValue('font-size'));
      document.documentElement.style.fontSize = (currentSize + 2) + 'px';
    }

    // Funkcja do pomniejszania czcionki
    function decreaseFontSize() {
      const currentSize = parseFloat(window.getComputedStyle(document.documentElement).getPropertyValue('font-size'));
      document.documentElement.style.fontSize = (currentSize - 2) + 'px';
    }

    // Obsługa przycisków
    document.getElementById('increaseBtn').addEventListener('click', increaseFontSize);
    document.getElementById('decreaseBtn').addEventListener('click', decreaseFontSize);
