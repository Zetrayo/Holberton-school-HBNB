// Utility function to get the value of a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Function to check user authentication
function checkAuthentication() {
    const loginLink = document.getElementById('login-link'); // Adjust ID if needed
    const token = getCookie('jwt_token'); // Replace 'jwt_token' with the actual cookie name for your JWT

    if (token) {
        // User is authenticated; hide the login link
        if (loginLink) {
            loginLink.style.display = 'none';
        }
    } else {
        // User is not authenticated; show the login link
        if (loginLink) {
            loginLink.style.display = 'block';
        }
    }
}

async function fetchPlaces() {
    const placesList = document.getElementById('places-list'); // Container to display places
    const token = getCookie('jwt_token'); // Replace 'jwt_token' with the actual cookie name

    try {
        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // Include the JWT token in the Authorization header if it exists
                ...(token && { 'Authorization': `Bearer ${token}` }),
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const places = await response.json();

        // Populate the places list dynamically
        if (placesList && Array.isArray(places)) {
            placesList.innerHTML = ''; // Clear any existing content
            places.forEach(place => {
                const placeItem = document.createElement('div');
                placeItem.className = 'place-item'; // Optional: Add a class for styling
                placeItem.innerHTML = `
                    <h3>${place.name}</h3>
                    <p>${place.description}</p>
                    <p>Price: $${place.price}</p>
                `;
                placesList.appendChild(placeItem);
            });
        }
    } catch (error) {
        console.error('Error fetching places:', error);

        if (placesList) {
            placesList.innerHTML = `<p class="error">Unable to fetch places. Please try again later.</p>`;
        }
    }
}

// Run the authentication check on page load
document.addEventListener('DOMContentLoaded', checkAuthentication);
