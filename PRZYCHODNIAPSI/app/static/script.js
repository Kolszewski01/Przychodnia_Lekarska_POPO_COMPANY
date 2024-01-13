document.addEventListener('DOMContentLoaded', function() {
    var myButton = document.getElementById('logout-form');

    if (myButton) {
        myButton.addEventListener('click', function() {
            showAlert();
        });
    }

    function showAlert() {
        alert('Hello! This is a simple alert.');
    }
});
