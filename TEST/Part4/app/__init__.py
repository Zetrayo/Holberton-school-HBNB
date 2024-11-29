# app/__init__.py
from flask import Flask
from flask_restx import Api
from config import config  # Import the config dictionary
from extensions import db, bcrypt, jwt
from flask_jwt_extended import JWTManager

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # Load the appropriate config based on the name

    app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET_KEY']
    jwt.init_app(app)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Create the API and add namespaces
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Import namespaces after initializing extensions to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenity_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as review_ns
    from app.api.v1.auth import api as auth_ns

    # Add namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app