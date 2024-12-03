#!/usr/bin/python3

# Import necessary modules and components
from flask import render_template  # To render HTML templates
from app import create_app  # Import the app creation function
from extensions import db  # Import the database extension
from app.models.user import User  # Import User model for database operations
from app.models.amenity import Amenity  # Import Amenity model for database operations
from app.models.place import Place  # Import Place model for database operations
from app.models.review import Review  # Import Review model for database operations

# Create the app instance using the create_app function
app = create_app()

# Create all tables if they do not already exist (inside app context)
with app.app_context():
    db.create_all()  # Creates the database tables for the models

# Route for serving the main index page
@app.route('/index')
def index():
    return render_template('index.html')  # Renders 'index.html' from the templates folder

# Route for serving the place details page
@app.route('/place/place.html')
def place():
    return render_template('/place/place.html')  # Renders 'place.html' from the 'place' folder in templates

# Route for serving the login page
@app.route('/auth/login.html')
def login():
    return render_template('auth/login.html')  # Renders the login page from the 'auth' folder in templates

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run()  # Starts the Flask application
