    // Check if the user is logged in
    const isLoggedIn = localStorage.getItem('access_token') !== null;

    // Get references to the buttons
    const loginButton = document.getElementById('loginButton');
    const logoutButton = document.getElementById('logoutButton');

    // Toggle button visibility based on the login status
    if (isLoggedIn) {
        logoutButton.style.display = 'block';
        loginButton.style.display = 'none';
    } else {
        loginButton.style.display = 'block';
        logoutButton.style.display = 'none';
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

