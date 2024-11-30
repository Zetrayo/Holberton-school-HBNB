from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from extensions import db, bcrypt, jwt
from flask_jwt_extended import JWTManager

# Initialize JWTManager instance
jwt = JWTManager()

def create_app(config=DevelopmentConfig):
    # Create the Flask app instance
    app = Flask(__name__)

    # Load the configuration settings from the specified config object
    app.config.from_object(config)

    # Set the JWT_SECRET_KEY for JWT operations
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with an actual secret key

    # Initialize the JWTManager with the app
    jwt.init_app(app)

    # Initialize other extensions (database, bcrypt, etc.)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)  # Redundant call here, can be removed as it's already initialized earlier

    # Create the API object with version and description
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Import namespaces after extensions are initialized to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenity_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as review_ns
    from app.api.v1.auth import api as auth_ns

    # Add namespaces to the API with specific URL paths
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Return the Flask app instance
    return app
