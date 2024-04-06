document.getElementById('reservationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const parkingSpot = document.getElementById('parkingSpot').value;
    const reservationDate = document.getElementById('reservationDate').value;
    const reservationTime = document.getElementById('reservationTime').value;
    
    // Assuming the API expects a dateTime format and user ID
    const dateTime = `${reservationDate}T${reservationTime}`;
    const userId = "user123"; // This should come from your user session

    fetch('http://localhost:8000/parking/reservations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userId: userId,
            parkingSpotId: parkingSpot,
            dateTime: dateTime,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Reservation Success:', data);
        alert('Reservation successful!');
        // Redirect or update the page as needed
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Reservation failed.');
    });
});
