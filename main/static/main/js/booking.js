function submitAppointmentForm(specialistId) {
    const form = document.getElementById('booking-form');
    const data = new FormData(form);
    data.append('specialist_id', specialistId);

    fetch(`/booking/${specialistId}/`, {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('booking-response').innerText = data.error;
        } else {
            document.getElementById('booking-response').innerText = data.message;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('booking-response').innerText = 'Помилка при бронюванні. Спробуйте знову.';
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
