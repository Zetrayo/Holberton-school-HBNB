#!/usr/bin/python3

from flask import render_template
from app import create_app
from extensions import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

# Create the app instance
app = create_app()

# Debug: Ensure the app is being created
print("Flask app created")

# Create all tables if they do not exist (inside app context)
with app.app_context():
    db.create_all()

# Route to serve the HTML file
@app.route('/')
def home():
    print("Rendering index.html")
    return render_template('index.html')  # Renders 'index.html' from the 'templates' folder

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
