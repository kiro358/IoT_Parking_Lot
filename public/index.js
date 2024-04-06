document.addEventListener('DOMContentLoaded', () => {
    const isLoggedIn = localStorage.getItem('access_token') !== null;
    toggleButtons(isLoggedIn);

    if (isLoggedIn) {
        // Assuming the user's ID is stored in localStorage for simplicity
        const userId = localStorage.getItem('user_id');
        fetchUserReservations(userId);
        const dummyReservations = getDummyReservations();
        displayReservations(dummyReservations);
    }
});

function toggleButtons(isLoggedIn) {
    const loginButton = document.getElementById('loginButton');
    const logoutButton = document.getElementById('logoutButton');
    const findparkingButton = document.getElementById('findparkingButton');

    if (isLoggedIn) {
        loginButton.style.display = 'none';
        logoutButton.style.display = 'block';
        findparkingButton.style.display = 'block';
    } else {
        loginButton.style.display = 'block';
        logoutButton.style.display = 'none';
        findparkingButton.style.display = 'none';
    }
}

async function fetchUserReservations(userId) {
    const reservationsResponse = await fetch(`/users/${userId}/reservations`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
    });

    if (reservationsResponse.ok) {
        const reservations = await reservationsResponse.json();
        displayReservations(reservations);
    } else {
        console.error('Failed to fetch reservations.');
    }
}

function getDummyReservations() {
    // Current time in milliseconds for comparison
    const now = new Date().getTime();

    return [
        {
            reservation_id: "res101",
            lot_id: "1",
            spot_id: "101",
            duration: 2,
            current_pricing: 10,
            end_time: new Date(now + 2 * 60 * 60 * 1000).toISOString(), // 2 hours from now
        },
        {
            reservation_id: "res102",
            lot_id: "1",
            spot_id: "102",
            duration: 3,
            current_pricing: 15,
            end_time: new Date(now - 1 * 60 * 60 * 1000).toISOString(), // 1 hour ago
        },
        {
            reservation_id: "res103",
            lot_id: "2",
            spot_id: "205",
            duration: 1.5,
            current_pricing: 7,
            end_time: new Date(now + 24 * 60 * 60 * 1000).toISOString(), // 24 hours from now
        },
    ];
}

function displayReservations(reservations) {
    const currentReservations = reservations.filter(isCurrentReservation);
    const pastReservations = reservations.filter(reservation => !isCurrentReservation(reservation));

    if (currentReservations.length > 0) {
        displayReservationSection('Current Reservations', currentReservations);
    }
    
    if (pastReservations.length > 0) {
        displayReservationSection('Past Reservations', pastReservations);
    }
}

function isCurrentReservation(reservation) {
    // Assuming reservation.end_time is the timestamp in milliseconds when the reservation ends
    // This will need to be adjusted based on how your reservation timing is structured
    return new Date(reservation.end_time).getTime() > Date.now();
}

function displayReservationSection(title, reservations) {
    // Create a title for the section
    const sectionTitle = document.createElement('h2');
    sectionTitle.textContent = title;
    document.body.appendChild(sectionTitle);
    
    // Create the reservations table
    const reservationsTable = document.createElement('table');
    reservationsTable.style.width = '100%'; // Adjust styling as needed
    reservationsTable.innerHTML = `
        <tr>
            <th style="text-align: left;">Reservation ID</th>
            <th style="text-align: left;">Lot ID</th>
            <th style="text-align: left;">Spot ID</th>
            <th style="text-align: left;">Duration</th>
            <th style="text-align: left;">Pricing</th>
        </tr>
    `;
    
    reservations.forEach(reservation => {
        const row = reservationsTable.insertRow(-1);
        row.innerHTML = `
            <td>${reservation.reservation_id}</td>
            <td>${reservation.lot_id}</td>
            <td>${reservation.spot_id}</td>
            <td>${reservation.duration} hours</td>
            <td>${reservation.current_pricing}</td>
        `;
    });
    
    document.body.appendChild(reservationsTable);
}


// Add click event listener for the logout button
logoutButton.addEventListener('click', function() {
    // Remove the token from localStorage
    localStorage.removeItem('access_token');

    // Optionally, refresh the page to update UI
    window.location.reload();
});

// Add click event listener for the login button (assuming it redirects to a login page)
loginButton.addEventListener('click', function() {
    window.location.href = '/login';
});

findparkingButton.addEventListener('click', function() {
    window.location.href = '/find_parking';
});

