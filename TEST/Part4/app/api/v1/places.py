#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('places', description='Place operations')

# Model for creating or updating a Place
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
    @jwt_required()  # JWT authorization check
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place with authorization token"""
        place_data = api.payload
        current_user = get_jwt_identity()  # Get the current user from the JWT token
        
        # Ensure the owner_id matches the current user
        if place_data.get('owner_id') != current_user:
            return {'error': 'Unauthorized to create place for another user'}, 403
        
        try:
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
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Error: {e}")  # For debugging purposes
            return {'message': 'Internal Server Error'}, 500

    @jwt_required()  # JWT authorization for fetching the places
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places for the authenticated user"""
        current_user = get_jwt_identity()
        places = facade.get_places_by_user(current_user)  # Fetch places for the current user
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
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
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

    @jwt_required()
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update place details"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if place.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403
        # Logic for updating place would go here
        return {'message': 'Place updated successfully'}, 200
