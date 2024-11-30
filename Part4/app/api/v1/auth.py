from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

# Define the namespace for authentication-related operations
api = Namespace('auth', description='Authentication operations')

# Define the model for login input validation and API documentation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)  # Validate input data against the defined model
    def post(self):
        """
        Authenticate a user and return a JWT access token if credentials are valid.
        """
        credentials = api.payload  # Extract email and password from the request payload

        # Attempt to retrieve the user by their email address
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            # Return an error if the user is not found or the password is incorrect
            return {'error': 'Invalid credentials'}, 401

        # Create a JWT token with user identity, including email and admin status
        access_token = create_access_token(identity={'email': str(user.email), 'is_admin': user.is_admin})

        # Return the generated token with a successful response
        return {'access_token': access_token}, 200
