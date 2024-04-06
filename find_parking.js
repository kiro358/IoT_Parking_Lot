document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/parking/spots/available')
    .then(response => response.json())
    .then(data => {
        const parkingSpotsSelect = document.getElementById('parkingSpot');
        data.forEach(spot => {
            let option = new Option(`Spot ${spot.id} - ${spot.location}`, spot.id);
            parkingSpotsSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));
});
