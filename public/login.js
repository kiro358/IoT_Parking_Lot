document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission.

        // Extract data from the form.
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,  // Assuming the email is used as the username
                password: password,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Invalid credentials'); // Or use response data to show more detailed error
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Handle success, for example, redirecting to another page or showing a success message.
            window.location.href = '/';
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors, for example, showing an error message to the user.
            alert('Failed to login: Invalid credentials'); // Simple error feedback
        });
    });
});
