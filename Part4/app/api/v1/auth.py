#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation (searching by user id)
login_model = api.model('Login', {
    'id': fields.String(required=True, description='User ID'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        credentials = api.payload  # Get the user id and password from the request payload
        user = facade.get_user(credentials['id'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        return {'access_token': access_token}, 200
