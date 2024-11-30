// Function to extract the "place_id" query parameter from the URL
function getPlaceIdFromUrl() {
    const params = new URLSearchParams(window.location.search);  // Get URL search parameters
    return params.get('place_id'); // Retrieves the "place_id" query parameter value
}

// Function to retrieve a cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;  // Append semicolon to the cookie string for easy parsing
    const parts = value.split(`; ${name}=`);  // Split cookies at the specific name
    if (parts.length === 2) {
        return parts.pop().split(';').shift();  // Return cookie value if found
    }
    return null;  // Return null if cookie is not found
}

// Asynchronous function to fetch place details from the server
async function fetchPlaceDetails(placeId) {
    const token = getCookie('token');  // Retrieve the user's authentication token from cookies
    try {
        // Sending a GET request to the server to fetch place details by ID
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',  // Setting content type to JSON
                ...(token && { 'Authorization': `Bearer ${token}` }),  // If token exists, add it in Authorization header
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);  // Throw error if response is not OK
        }
        return await response.json();  // Parse and return the JSON response
    } catch (error) {
        console.error('Error fetching place details:', error);  // Log error if something goes wrong
        return null;  // Return null in case of error
    }
}

// Function to display the place details on the page
function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    placeDetailsSection.innerHTML = '';  // Clear any existing content
    if (!place) {
        placeDetailsSection.innerHTML = '<p>Unable to load place details. Please try again later.</p>';
        return;
    }

    // Create elements for place title, description, price, location, and amenities
    const titleElement = document.createElement('h1');
    titleElement.textContent = place.title;

    const descriptionElement = document.createElement('p');
    descriptionElement.innerHTML = `<strong>Description:</strong> ${place.description || 'No description available.'}`;

    const priceElement = document.createElement('p');
    priceElement.innerHTML = `<strong>Price:</strong> $${place.price.toFixed(2)} per night`;

    const locationElement = document.createElement('p');
    locationElement.innerHTML = `<strong>Location:</strong> (${place.latitude.toFixed(2)}, ${place.longitude.toFixed(2)})`;

    const amenitiesElement = document.createElement('div');
    amenitiesElement.innerHTML = `<strong>Amenities:</strong>`;
    const amenitiesList = document.createElement('ul');
    if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(amenity => {
            const listItem = document.createElement('li');
            listItem.textContent = amenity;
            amenitiesList.appendChild(listItem);
        });
    } else {
        amenitiesList.innerHTML = '<li>No amenities listed.</li>';
    }

    // Append all created elements to the place details section
    amenitiesElement.appendChild(amenitiesList);
    placeDetailsSection.appendChild(titleElement);
    placeDetailsSection.appendChild(descriptionElement);
    placeDetailsSection.appendChild(priceElement);
    placeDetailsSection.appendChild(locationElement);
    placeDetailsSection.appendChild(amenitiesElement);
}

// Function to display reviews on the page
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h3>Reviews</h3>';  // Clear and add a heading for reviews
    const reviewsList = document.createElement('ul');
    if (reviews && reviews.length > 0) {
        reviews.forEach(review => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${review.user}</strong>: ${review.text}`;
            reviewsList.appendChild(listItem);
        });
    } else {
        reviewsList.innerHTML = '<li>No reviews yet.</li>';
    }
    reviewsSection.appendChild(reviewsList);
}

// Function to show/hide the "Add Review" form based on authentication status
function toggleAddReviewForm(isAuthenticated) {
    const reviewForm = document.getElementById('add-review-form');
    reviewForm.style.display = isAuthenticated ? 'block' : 'none';  // Display the form only if the user is authenticated
}

// Event listener to run the code when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', async () => {
    const placeId = getPlaceIdFromUrl();  // Get place ID from URL
    if (!placeId) {
        console.error('No place ID found in the URL.');  // Log error if no place ID is found
        return;
    }

    const token = getCookie('token');  // Retrieve the token to check if the user is authenticated
    const isAuthenticated = !!token;  // Check if token exists, indicating authentication
    toggleAddReviewForm(isAuthenticated);  // Show or hide the review form based on authentication

    const placeDetails = await fetchPlaceDetails(placeId);  // Fetch place details using the place ID
    if (placeDetails) {
        displayPlaceDetails(placeDetails);  // If place details are fetched, display them
        displayReviews(placeDetails.reviews || []);  // Display reviews, or show a message if no reviews exist
    }
});
