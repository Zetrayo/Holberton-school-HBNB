from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.models.user import User

# Define a namespace for user-related operations
api = Namespace('users', description='User operations')

# User model for input validation and API documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)  # Validate input against the user model
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """
        Create a new user.
        Ensures the email is unique and hashes the password before saving the user.
        """
        user_data = api.payload
        # Check if the email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Hash the password and create the user
        user_data['password'] = User.hash_password(user_data['password'])
        new_user = facade.create_user(user_data)

        # Return the created user's ID and a success message
        return {
            'id': new_user.id,
            'message': 'User successfully created',
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve a list of all users.
        Returns basic user information excluding sensitive details.
        """
        users = facade.user_repo.get_all()  # Fetch all users from the repository
        # Serialize and return the list of users
        return [
            {'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email}
            for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve a specific user by their ID.
        Returns a 404 error if the user is not found.
        """
        user = facade.get_user(user_id)  # Fetch user by ID
        if not user:
            return {'error': 'User not found'}, 404

        # Serialize and return the user details
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)  # Validate input for updating a user
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update a user's details.
        Validates the input and updates the user if they exist.
        """
        user_data = api.payload
        updated_user = facade.update_user(user_id, user_data)  # Attempt to update the user

        if not updated_user:
            return {'error': 'User not found'}, 404

        # Serialize and return the updated user details
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
