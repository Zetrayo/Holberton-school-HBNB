document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form'); 
    const token = getCookie('access_token'); // Replace 'jwt_token' with the actual name of your JWT cookie

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Handle form submission
            async function loginUser(email, password) {
                const response = await fetch('https://your-api-url/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                // Handle the response
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed: ' + response.statusText);
                }
            }
        });
    }
});
