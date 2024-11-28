#!/usr/bin/python3 

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):  # Make sure to inherit from Config
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
