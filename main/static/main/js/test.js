// Отримуємо модальне вікно
var modal = document.getElementById("result-modal");

// Отримуємо кнопку, яка відкриває модальне вікно
var btn = document.getElementById("result-button");

// Отримуємо елемент <span>, який закриває модальне вікно
var span = document.getElementsByClassName("close")[0];

// При натисканні на кнопку відкриваємо модальне вікно
btn.onclick = function() {
    modal.style.display = "block";
}

// При натисканні на <span> (x), закриваємо модальне вікно
span.onclick = function() {
    modal.style.display = "none";
}

// При натисканні будь-де поза модальним вікном, закриваємо його
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}