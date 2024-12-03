// Utility function to get the value of a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift(); // Return the cookie value if found
    return null; // Return null if the cookie doesn't exist
}

// Function to check user authentication and adjust login link visibility
function checkAuthentication() {
    const loginLink = document.getElementById('login-link'); // Get the login link element
    const token = getCookie('jwt'); // Retrieve JWT token from cookies

    if (token) {
        // If the user is authenticated (JWT exists), hide the login link
        if (loginLink) {
            loginLink.style.display = 'none';
        }
    } else {
        // If the user is not authenticated, show the login link
        if (loginLink) {
            loginLink.style.display = 'block';
        }
    }
}

// Function to fetch and display a list of places from the server
async function fetchPlaces() {
    const placesList = document.getElementById('places-list'); // Container to display places
    const token = getCookie('jwt'); // Retrieve JWT token for authentication if available

    try {
        const response = await fetch('/api/v1/places', {
            method: 'GET', // Make a GET request to fetch places
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` }), // Include token in header if authenticated
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`); // Handle errors if response is not OK
        }

        const places = await response.json(); // Parse the response as JSON

        if (placesList && Array.isArray(places)) {
            placesList.innerHTML = ''; // Clear any existing places before adding new ones

            if (places.length === 0) {
                placesList.innerHTML = '<p>No places available.</p>'; // Show message if no places are available
            } else {
                // Loop through the places array and display each place's details
                places.forEach(place => {
                    const placeItem = document.createElement('div');
                    placeItem.className = 'place-item'; // Optional: Add a class for styling
                    placeItem.dataset.price = place.price; // Store the place's price as a data attribute for filtering

                    placeItem.innerHTML = `
                        <h3>${place.title}</h3>
                        <p><strong>Description:</strong> ${place.description || "No description available."}</p>
                        <p><strong>Price:</strong> $${place.price.toFixed(2)} per night</p>
                        <p><strong>Location:</strong> (${place.latitude.toFixed(2)}, ${place.longitude.toFixed(2)})</p>
                        <ul>
                            <strong>Amenities:</strong>
                            ${place.amenities && place.amenities.length > 0
                                ? place.amenities.map(amenity => `<li>${amenity}</li>`).join("") // Loop through amenities
                                : "<li>No amenities listed</li>"}
                        </ul>
                    `;

                    placesList.appendChild(placeItem); // Append the new place item to the list
                });
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error); // Log errors to the console

        if (placesList) {
            placesList.innerHTML = '<p class="error">Unable to fetch places. Please try again later.</p>'; // Show error message to user
        }
    }
}

// Function to set up the price filter based on user selection
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter'); // Get the price filter dropdown
    const placesList = document.getElementById('places-list'); // Get the container to display places

    priceFilter.addEventListener('change', () => {
        const selectedPrice = parseFloat(priceFilter.value); // Get the selected price range

        const places = placesList.getElementsByClassName('place-item'); // Get all place items for filtering

        // Loop through all place items and filter based on price
        Array.from(places).forEach(placeItem => {
            const placePrice = parseFloat(placeItem.dataset.price); // Get the price of the place from data-price attribute

            // Show or hide places based on the selected price range
            if (selectedPrice === 0 || placePrice <= selectedPrice) {
                placeItem.style.display = ''; // Show the place if it matches the filter
            } else {
                placeItem.style.display = 'none'; // Hide the place if it doesn't match
            }
        });
    });
}

// Event listener to run functions on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication(); // Check user authentication status on page load
    fetchPlaces();  // Fetch and display places from the server
    setupPriceFilter(); // Set up the price filter functionality
});
