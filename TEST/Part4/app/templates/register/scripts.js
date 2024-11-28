document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form'); 
    const token = getCookie('access_token'); // Replace 'jwt_token' with the actual name of your JWT cookie

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Handle form submission

            const first_name = document.getElementById('first_name').value; // Fetch the first_name from the form to send it to the API
            const last_name = document.getElementById('last_name').value // Fetch the last_name from the form to send it to the API
            const email = document.getElementById('email').value; // Fetch the mail from the form to send it to the API
            const password = document.getElementById('password').value // Fetch the password from the form to send it to the API


            async function registerUser(first_name, last_name, email, password) {
                const response = await fetch('http://localhost:5000/api/v1/user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({first_name, last_name, email, password })
                });
                // Handle the response
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    alert('Register failed: ' + response.statusText);
                }
            }
            await registerUser(first_name, last_name, email, password); // Call the created function
        });
    }
});
