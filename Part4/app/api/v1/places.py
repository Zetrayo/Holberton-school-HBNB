from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Define a namespace for place-related operations
api = Namespace('places', description='Place operations')

# Define the model for creating or updating a place
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()  # Require a valid JWT for authorization
    @api.expect(place_model)  # Validate input data against the defined place model
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new place for the authenticated user.
        Requires the `owner_id` in the request payload to match the authenticated user's ID.
        """
        place_data = api.payload
        current_user = get_jwt_identity()  # Get the current authenticated user

        # Ensure the owner ID in the request matches the current user's ID
        if place_data.get('owner_id') != current_user:
            return {'error': 'Unauthorized to create place for another user'}, 403

        try:
            # Attempt to create the new place
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.user.id,
                'amenities': new_place.amenities
            }, 201
        except ValueError as e:
            # Handle invalid input errors
            return {'error': str(e)}, 400
        except Exception as e:
            # Log unexpected errors for debugging and return a generic error message
            print(f"Error: {e}")
            return {'message': 'Internal Server Error'}, 500

    @jwt_required()  # Require a valid JWT for authorization
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places for the authenticated user.
        Only places associated with the user's ID will be returned.
        """
        current_user = get_jwt_identity()  # Get the current authenticated user
        places = facade.get_places_by_user(current_user)  # Fetch places linked to the user
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'amenities': place.amenities
            }
            for place in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details of a specific place by its ID.
        """
        place = facade.get_place(place_id)
        if not place:
            # Return a 404 error if the place is not found
            return {'error': 'Place not found'}, 404

        # Return the place details
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.user.id,
            'amenities': place.amenities
        }, 200

    @jwt_required()  # Require a valid JWT for authorization
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """
        Update details of a specific place.
        Only the owner of the place can update its details.
        """
        current_user = get_jwt_identity()  # Get the current authenticated user
        place = facade.get_place(place_id)

        if not place:
            # Return a 404 error if the place is not found
            return {'error': 'Place not found'}, 404

        if place.user.id != current_user:
            # Return a 403 error if the authenticated user is not the owner of the place
            return {'error': 'Unauthorized action'}, 403

        # Place update logic would go here (not implemented in this example)
        return {'message': 'Place updated successfully'}, 200
