import os

# Base configuration class, containing common settings
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Secret key for session management and CSRF protection
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')  # JWT secret key for token generation
    DEBUG = False  # Disable debugging by default

# Development-specific configuration, inherits from the base Config class
class DevelopmentConfig(Config):  
    DEBUG = True  # Enable debugging in development environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'  # Database URI for SQLite in development
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable SQLAlchemy modification tracking to save resources

# Dictionary to easily select different configurations
config = {
    'development': DevelopmentConfig,  # Configuration for development environment
    'default': DevelopmentConfig  # Default configuration (usually for production, but here it's development)
}
