from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

# Create a namespace for user operations
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Route for handling multiple users
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Create a new user and return a JWT token"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Hash the password before storing it
        user_data['password'] = User.hash_password(user_data['password'])
        new_user = facade.create_user(user_data)

        # Create and return a token for the new user
        access_token = create_access_token(identity={'email': str(new_user.email), 'is_admin': new_user.is_admin})
        
        return {
            'id': new_user.id,
            'message': 'User successfully created',
            'access_token': access_token
        }, 201

    @jwt_required()  # Protect this route with JWT authentication
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of users (admin only)"""
        current_user = get_jwt_identity()
        
        # Check if the current user is an admin
        if not facade.is_admin(current_user):
            return {'error': 'Unauthorized'}, 403
        
        users = facade.user_repo.get_all()
        return [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users], 200

# Route for handling individual users by ID
@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()  # Protect this route with JWT authentication
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a user by ID"""
        current_user = get_jwt_identity()
        
        # Check if the current user can access this user's information
        if current_user != user_id and not facade.is_admin(current_user):
            return {'error': 'Unauthorized'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()  # Protect this route with JWT authentication
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user's information"""
        current_user = get_jwt_identity()
        
        # Check if the current user can update this user's information
        if current_user != user_id and not facade.is_admin(current_user):
            return {'error': 'Unauthorized'}, 403
        
        user_data = api.payload
        
        # Hash the password again if it's being updated
        if 'password' in user_data:
            user_data['password'] = User.hash_password(user_data['password'])
        
        updated_user = facade.update_user(user_id, user_data)
        
        if not updated_user:
            return {'error': 'User not found'}, 404
        
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200

    @jwt_required()  # Protect this route with JWT authentication
    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        current_user = get_jwt_identity()
        
        # Check if the current user can delete this user's account
        if current_user != user_id and not facade.is_admin(current_user):
            return {'error': 'Unauthorized'}, 403
        
        if facade.delete_user(user_id):
            return {'message': 'User successfully deleted'}, 200
        
        return {'error': 'User not found'}, 404