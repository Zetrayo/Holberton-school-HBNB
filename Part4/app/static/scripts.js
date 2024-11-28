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
    const token = getCookie('jwt'); // Adjust cookie name if needed (it was 'jwt_token' before, now we assume it's 'jwt')

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
    const token = getCookie('jwt'); // Adjust cookie name if needed

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
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const places = await response.json();

        // Populate the places list dynamically
        if (placesList && Array.isArray(places)) {
            placesList.innerHTML = ''; // Clear any existing content before adding new places

            if (places.length === 0) {
                placesList.innerHTML = '<p>No places available.</p>';
            } else {
                places.forEach(place => {
                    const placeItem = document.createElement('div');
                    placeItem.className = 'place-item'; // Optional: Add a class for styling
                    placeItem.dataset.price = place.price; // Store the price in the data attribute

                    placeItem.innerHTML = `
                        <h3>${place.title}</h3>
                        <p><strong>Description:</strong> ${place.description || "No description available."}</p>
                        <p><strong>Price:</strong> $${place.price.toFixed(2)} per night</p>
                        <p><strong>Location:</strong> (${place.latitude.toFixed(2)}, ${place.longitude.toFixed(2)})</p>
                        <ul>
                            <strong>Amenities:</strong>
                            ${place.amenities && place.amenities.length > 0
                                ? place.amenities.map(amenity => `<li>${amenity}</li>`).join("")
                                : "<li>No amenities listed</li>"}
                        </ul>
                    `;

                    // Append the dynamically created place item to the list
                    placesList.appendChild(placeItem);
                });
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);

        if (placesList) {
            placesList.innerHTML = '<p class="error">Unable to fetch places. Please try again later.</p>';
        }
    }
}

// Event listener for the price filter dropdown
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter'); // Price filter dropdown
    const placesList = document.getElementById('places-list'); // Container to display places

    priceFilter.addEventListener('change', () => {
        const selectedPrice = parseFloat(priceFilter.value); // Get the selected price range

        const places = placesList.getElementsByClassName('place-item'); // All place items

        // Loop through all place items and filter based on price
        Array.from(places).forEach(placeItem => {
            const placePrice = parseFloat(placeItem.dataset.price); // Get the price of each place from data-price attribute

            if (selectedPrice === 0 || placePrice <= selectedPrice) {
                placeItem.style.display = ''; // Show the place if it matches the filter
            } else {
                placeItem.style.display = 'none'; // Hide the place if it doesn't match
            }
        });
    });
}

// Run the authentication check and setup filter on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    fetchPlaces();  // Fetch and display places once the page loads
    setupPriceFilter(); // Setup the price filter functionality
});
