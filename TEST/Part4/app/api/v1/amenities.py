from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place to which this amenity belongs')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()  # Protect this route with JWT authentication
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity for a specific place"""
        current_user = get_jwt_identity()  # Get the current user's identity
        amenity_data = api.payload
        
        # Check if the user is the owner of the place
        place = facade.get_place(amenity_data['place_id'])
        if not place or place.owner_id != current_user and  not facade.is_admin(current_user):
            return {'error': 'Unauthorized: You do not own this place'}, 403
        
        existing_amenity = facade.get_amenity(amenity_data['name'], amenity_data['place_id'])
        if existing_amenity:
            return {'error': 'Amenity already exists for this place'}, 400
        
        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'place_id': new_amenity.place_id
        }, 201

    @jwt_required()  # Protect this route with JWT authentication
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @jwt_required()  # Protect this route with JWT authentication
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        current_user = get_jwt_identity()  # Get the current user's identity
        amenity = facade.get_amenity(amenity_id)
        
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Optionally check if the user is allowed to view this amenity (e.g., they own it)
        if amenity.place.owner_id != current_user and not facade.is_admin(current_user):
            return {'error': 'Unauthorized: You do not own this place'}, 403
        
        return {'id': amenity.id, 'name': amenity.name}, 200

    @jwt_required()  # Protect this route with JWT authentication
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()  # Get the current user's identity
        
        # Check if the user is allowed to update this amenity (if they own it or are an admin)
        amenity = facade.get_amenity(amenity_id)
        
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        if amenity.place.owner_id != current_user and not facade.is_admin(current_user):
            return {'error': 'Unauthorized: You do not own this place'}, 403
        
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200