document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form'); 

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Fetch form data
            const first_name = document.getElementById('first_name').value; // User's first name
            const last_name = document.getElementById('last_name').value;   // User's last name
            const email = document.getElementById('email').value;          // User's email
            const password = document.getElementById('password').value;    // User's password

            // Function to handle user registration
            async function registerUser(first_name, last_name, email, password) {
                const response = await fetch('http://localhost:5000/api/v1/user/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ first_name, last_name, email, password })
                });

                // Handle the server response
                if (response.ok) {
                    const data = await response.json();

                    // Redirect user to the desired page
                    window.location.href = 'place.html';
                } else {
                    alert('Registration failed: ' + response.statusText);
                }
            }

            // Call the registerUser function
            await registerUser(first_name, last_name, email, password);
        });
    }
});
