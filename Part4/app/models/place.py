from extensions import db
from sqlalchemy.orm import relationship
from .baseclass import BaseModel

class Place(BaseModel):
    """Represents a place where users can stay. Inherits from BaseModel."""
    
    __tablename__ = 'places'  # Name of the table in the database

    title = db.Column(db.String(100), nullable=False)  
    # Title of the place (e.g., name of the property), cannot be null

    description = db.Column(db.String(500), nullable=True)  
    # A brief description of the place, can be null (optional field)

    price = db.Column(db.Float, nullable=False)  
    # Price per night for staying at the place, cannot be null

    latitude = db.Column(db.Float, nullable=False)  
    # Latitude coordinate for the location of the place, cannot be null

    longitude = db.Column(db.Float, nullable=False)  
    # Longitude coordinate for the location of the place, cannot be null

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  
    # Foreign key linking to the 'users' table (representing the owner of the place), cannot be null

    user = db.relationship('User', back_populates='places')  
    # Relationship to the User model, where 'User' is the owner of the place, back_populates ensures bidirectional relationship

    reviews = db.relationship('Review', back_populates='place')  
    # Relationship to the Review model, to retrieve all reviews associated with the place, back_populates links to 'place' in Review model

    amenities = db.relationship('Amenity', secondary='place_amenities', back_populates='places')  
    # Many-to-many relationship with the Amenity model, facilitated by the 'place_amenities' association table
