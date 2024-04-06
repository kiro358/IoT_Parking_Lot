document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Extract data from the form
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const fullName = document.getElementById('fullName').value;

        // Assume you split the full name into first and last names for the User model or adapt as necessary
        const [firstName, lastName] = fullName.split(' '); // Simple split, consider more robust handling

        // Prepare the data to be sent to the server
        const userData = {
            email: email,
            username: firstName, // Assuming the first name as the username, adjust as necessary
            password: password,
        };

        // Use the fetch API to send the data to your FastAPI backend
        fetch('/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success, e.g., redirecting to the login page or showing a success message
            window.location.href = '/login'; // Redirect to login on successful registration
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors, e.g., showing an error message to the user
        });
    });
});
