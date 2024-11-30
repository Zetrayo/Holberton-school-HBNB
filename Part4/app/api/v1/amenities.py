from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Define the namespace for amenity-related API operations
api = Namespace('amenities', description='Operations for managing amenities')

# Define the amenity model for input validation and API documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')  # Name field is required
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity.

        This endpoint allows the creation of a new amenity. If an amenity with
        the given name already exists, an error response is returned.
        """
        amenity_data = api.payload  # Retrieve the input data from the request
        existing_amenity = facade.get_amenity(amenity_data['name'])  # Check if amenity exists
        if existing_amenity:
            return {'error': 'Amenity exists already'}, 400
        new_amenity = facade.create_amenity(amenity_data)  # Create a new amenity
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.

        This endpoint fetches and returns all available amenities as a list.
        """
        amenities = facade.get_all_amenities()  # Retrieve all amenities
        return [{'name': amenity.name} for amenity in amenities], 200  # Format the response

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get details of a specific amenity by ID.

        This endpoint fetches and returns the details of an amenity
        identified by its ID. If the amenity is not found, a 404 response
        is returned.
        """
        amenity = facade.get_amenity(amenity_id)  # Retrieve amenity by ID
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200  # Return amenity details

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an existing amenity's information.

        This endpoint updates the details of an amenity identified by its ID.
        If the amenity does not exist, a 404 response is returned.
        """
        amenity_data = api.payload  # Retrieve the input data from the request
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)  # Update amenity details
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200  # Return updated details
