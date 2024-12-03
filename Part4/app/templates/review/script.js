// Function to retrieve the value of a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`; // Fetch all cookies into a string
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift(); // Return the cookie value if found
    return undefined; // Return undefined if the cookie is not found
}

// Function to extract the "placeId" parameter from the URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search); // Parse the query parameters
    return params.get('placeId'); // Return the value of "placeId"
}

// Function to make an AJAX request to submit a review
async function submitReview(token, placeId, reviewText) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
            },
            body: JSON.stringify({ placeId, reviewText }) // Send placeId and reviewText in the request body
        });

        handleResponse(response); // Handle the server response
    } catch (error) {
        alert('An error occurred while submitting your review. Please try again.');
        console.error(error);
    }
}

// Function to handle the server response for review submission
function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!'); // Display success message
        document.getElementById('review-text').value = ''; // Clear the form input
    } else {
        alert('Failed to submit review. Please check your input and try again.'); // Display error message
    }
}

// Function to check user authentication
function checkAuthentication() {
    const token = getCookie('LogedInToken'); // Get the token from cookies
    if (!token) {
        alert('You must be logged in to submit a review. Redirecting to login page.');
        window.location.href = 'index.html'; // Redirect unauthenticated users
    }
    return token; // Return the token for authenticated users
}

// Event listener to handle form submission when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form'); // Get the review form element

    const token = checkAuthentication(); // Check authentication and get the token
    const placeId = getPlaceIdFromURL(); // Extract the placeId from the URL

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent the default form submission behavior

            const reviewText = document.getElementById('review-text').value; // Get the review text from the form

            // Call the function to submit the review
            await submitReview(token, placeId, reviewText);
        });
    }
});