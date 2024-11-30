# extensions.py

# Import necessary extensions
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database interaction
from flask_bcrypt import Bcrypt  # Bcrypt for password hashing
from flask_jwt_extended import JWTManager  # JWTManager for JSON Web Token (JWT) handling

# Initialize JWT manager for token-based authentication
jwt = JWTManager()

# Initialize SQLAlchemy for ORM-based database interaction
db = SQLAlchemy()

# Initialize Bcrypt for securely hashing and checking passwords
bcrypt = Bcrypt()
