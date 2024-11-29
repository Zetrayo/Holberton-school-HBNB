from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask_jwt_extended import jwt_required

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Enregistrer une nouvelle commodité"""
        amenity_data = api.payload
        existing_amenity = facade.get_amenity(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity exists already'}, 400
        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id' : new_amenity.id,
            'name': new_amenity.name
            }, 201

    @jwt_required()
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Récupérer une liste de toutes les commodités"""
        amenities = facade.get_all_amenities()
        return [{'name': amenities.name} for amenities in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Obtient les details de commodités par ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Mis a jour de l'information d'un commodité"""
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'amenity not found'}, 404
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
