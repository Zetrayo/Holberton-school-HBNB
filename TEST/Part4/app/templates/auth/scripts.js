document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form'); 
    const token = getCookie('access_token'); // Replace 'jwt_token' with the actual name of your JWT cookie

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Handle form submission

            const email = document.getElementById('email').value; // Fetch the mail from the form to send it to the API
            const password = document.getElementById('password').value // Fetch the password from the form to send it to the API

            async function loginUser(email, password) {
                const response = await fetch('http://localhost:5000/api/v1/auth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                // Handle the response
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed: ' + response.statusText);
                }
            }
            await loginUser(email, password); // Call the function 
        });
    }
});
