from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Create a namespace for review operations
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'title': fields.String(required=True, description='Title of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (0-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Route for handling multiple reviews
@api.route('/')
class ReviewList(Resource):
    @jwt_required()  # Ensure that the user is authenticated to create a review
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()  # Get the current user's identity from the JWT token
        review_data['user_id'] = current_user  # Set the user_id to the current user's ID
        try:
            review = facade.create_review(review_data)  # Create a new review using the facade
            return {"message": "Review successfully created", "review_id": review.id}, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()  # Fetch all reviews from the repository
        return [self.serialize_review(review) for review in reviews], 200

    @staticmethod
    def serialize_review(review):
        """Serialize a review object into a dictionary format"""
        return {
            "id": review.id,
            "title": review.title,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        }

# Route for handling individual reviews by ID
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)  # Fetch the specific review by ID
        if review:
            return ReviewList.serialize_review(review), 200
        else:
            return {"error": "Review not found"}, 404

    @jwt_required()  # Ensure that the user is authenticated to update a review
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()  # Get the current user's identity from the JWT token
        review = facade.get_review(review_id)  # Fetch the specific review by ID
        if not review:
            return {"error": "Review not found"}, 404
        if str(review.user_id) != current_user:  # Check if the current user is authorized to update this review
            return {"error": "Unauthorized action"}, 403
        
        review_data = api.payload  # Get updated data from request payload
        try:
            updated_review = facade.update_review(review_id, review_data)  # Update the review using the facade
            return ReviewList.serialize_review(updated_review), 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()  # Ensure that the user is authenticated to delete a review
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()  # Get the current user's identity from the JWT token
        review = facade.get_review(review_id)  # Fetch the specific review by ID
        if not review:
            return {"error": "Review not found"}, 404
        if str(review.user_id) != current_user:  # Check if the current user is authorized to delete this review
            return {"error": "Unauthorized action"}, 403
        
        try:
            facade.delete_review(review_id)  # Delete the specified review using the facade
            return {"message": "Review deleted successfully"}, 200
        except ValueError:
            return {"error": "Review not found"}, 404

# Route for retrieving reviews associated with a specific place
@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)  # Fetch reviews associated with a specific place ID
        if reviews:
            return [ReviewList.serialize_review(review) for review in reviews], 200
        else:
            return {"error": "Place not found or no reviews for this place"}, 404