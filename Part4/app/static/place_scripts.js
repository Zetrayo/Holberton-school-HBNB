function getPlaceIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id'); // Retrieves the "place_id" query parameter
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

async function fetchPlaceDetails(placeId) {
    const token = getCookie('token'); // Retrieve the user's token from cookies
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` }),
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json(); // Parse and return JSON response
    } catch (error) {
        console.error('Error fetching place details:', error);
        return null;
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    placeDetailsSection.innerHTML = ''; // Clear existing content
    if (!place) {
        placeDetailsSection.innerHTML = '<p>Unable to load place details. Please try again later.</p>';
        return;
    }
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
    amenitiesElement.appendChild(amenitiesList);
    placeDetailsSection.appendChild(titleElement);
    placeDetailsSection.appendChild(descriptionElement);
    placeDetailsSection.appendChild(priceElement);
    placeDetailsSection.appendChild(locationElement);
    placeDetailsSection.appendChild(amenitiesElement);
}

function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h3>Reviews</h3>'; // Clear and add a heading
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

function toggleAddReviewForm(isAuthenticated) {
    const reviewForm = document.getElementById('add-review-form');
    reviewForm.style.display = isAuthenticated ? 'block' : 'none';
}

document.addEventListener('DOMContentLoaded', async () => {
    const placeId = getPlaceIdFromUrl();
    if (!placeId) {
        console.error('No place ID found in the URL.');
        return;
    }
    const token = getCookie('token');
    const isAuthenticated = !!token; // Check authentication status
    toggleAddReviewForm(isAuthenticated);
    const placeDetails = await fetchPlaceDetails(placeId);
    if (placeDetails) {
        displayPlaceDetails(placeDetails);
        displayReviews(placeDetails.reviews || []);
    }
});
