// Function to retrieve the value of a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`; // Fetch every cookies into a string
    const parts = value.split(`; ${name}=`); // Cut it by searched name
    if (parts.length === 2) return parts.pop().split(';').shift(); // if key exist return the value
    return undefined;
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    // Check if the token is already present in cookies
    const token = getCookie('LogedInToken');
    if (token) {
        console.log('User is already logged in. Redirecting...');
        window.location.href = 'place.html'; // Redirect the user if already logged in
        return; // Stop further execution of the code
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Get values from the login form
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Function to send login data to the server
            async function loginUser(email, password) {
                const response = await fetch('http://localhost:5000/api/v1/auth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                // Handle the server response
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `LogedInToken=${data.access_token}; path=/; SameSite=Strict`;
                    window.location.href = 'redirected.html';
                } else {
                    alert('Login failed: ' + response.statusText);
                }
            }

            // Call the loginUser function with form data
            await loginUser(email, password);
        });
    }
});
