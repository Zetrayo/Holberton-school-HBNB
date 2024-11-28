# app/__init__.py
from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from extensions import db, bcrypt, jwt
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt.init_app(app)

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Créer l'API et ajouter les namespaces
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Importer les namespaces après initialisation des extensions pour éviter les boucles
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenity
    from app.api.v1.places import api as place
    from app.api.v1.reviews import api as review
    from app.api.v1.auth import api as auth

    # Ajouter les namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity, path='/api/v1/amenities')
    api.add_namespace(review, path='/api/v1/reviews')
    api.add_namespace(place, path='/api/v1/places')
    api.add_namespace(auth, path='/api/v1/auth')

    return app
