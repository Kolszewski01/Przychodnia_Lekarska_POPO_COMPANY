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

// document.addEventListener("DOMContentLoaded", function () {
//     const container = document.getElementById('doctors-slider');
//     const images = container.getElementsByTagName('img');
//     const arrow = document.querySelector('.arrow');
//     let currentSlide = 0;
//
//     function showSlide(index) {
//         for (let i = 0; i < images.length; i++) {
//             images[i].style.transform = `translateY(-${index * 100}%)`;
//         }
//     }
//
//     function nextSlide() {
//         currentSlide = (currentSlide + 1) % images.length;
//         showSlide(currentSlide);
//     }
//
//     function prevSlide() {
//         currentSlide = (currentSlide - 1 + images.length) % images.length;
//         showSlide(currentSlide);
//     }
//
//     // Adding event listener for manual control using arrow
//     arrow.addEventListener('click', function () {
//         nextSlide();
//     });
//
//     // Adding event listeners for manual control using images
//     for (let i = 0; i < images.length; i++) {
//         images[i].addEventListener('click', function () {
//             nextSlide();
//         });
//     }
// });
