from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Define a namespace for review-related operations
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'title': fields.String(required=True, description='Title of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (0-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)  # Validate incoming data with the defined review model
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new review for a specific place.
        Validates the input payload before creating the review.
        """
        review_data = api.payload
        try:
            # Attempt to create the review
            review = facade.create_review(review_data)
            return {"message": "Review successfully created", "review_id": review.id}, 201
        except ValueError as e:
            # Handle invalid input errors
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.
        Returns serialized review data including associated metadata.
        """
        reviews = facade.get_all_reviews()
        return [self.serialize_review(review) for review in reviews], 200

    def serialize_review(self, review):
        """
        Helper function to serialize review data into a structured format.
        Includes all relevant review details along with timestamps.
        """
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

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Retrieve details of a specific review by its ID.
        Returns a 404 error if the review is not found.
        """
        review = facade.get_review(review_id)
        if review:
            return ReviewList.serialize_review(self, review), 200
        else:
            return {"error": "Review not found"}, 404

    @api.expect(review_model)  # Validate input data for updating the review
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update the details of an existing review.
        Requires valid review data in the payload.
        """
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            return ReviewList.serialize_review(self, updated_review), 200
        except ValueError as e:
            # Handle invalid input or update errors
            return {"error": str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete an existing review by its ID.
        Returns a success message or a 404 error if the review does not exist.
        """
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError:
            return {"error": "Review not found"}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve all reviews for a specific place by its ID.
        Returns a list of reviews or a 404 error if no reviews are found.
        """
        reviews = facade.get_reviews_by_place(place_id)
        if reviews:
            return [ReviewList.serialize_review(self, review) for review in reviews], 200
        else:
            return {"error": "Place not found or no reviews for this place"}, 404
