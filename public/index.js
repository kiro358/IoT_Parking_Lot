document.addEventListener('DOMContentLoaded', () => {
    const isLoggedIn = localStorage.getItem('access_token') !== null;
    toggleButtons(isLoggedIn);

    if (isLoggedIn) {
        // Assuming the user's ID is stored in localStorage for simplicity
        const userId = localStorage.getItem('user_id');
        fetchUserReservations(userId);
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

function displayReservations(reservations) {
    const reservationsTable = document.createElement('table');
    reservationsTable.innerHTML = `
        <tr>
            <th>Reservation ID</th>
            <th>Lot ID</th>
            <th>Spot ID</th>
            <th>Duration</th>
            <th>Pricing</th>
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

