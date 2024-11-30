from extensions import db
from .baseclass import BaseModel

class Review(BaseModel):
    """Represents a review for a place, inherited from BaseModel."""
    
    __tablename__ = 'reviews'  # Name of the table in the database

    title = db.Column(db.String(100), nullable=False)  
    # Title of the review (e.g., short headline), cannot be null

    text = db.Column(db.String(500), nullable=False)  
    # Text content of the review, cannot be null

    rating = db.Column(db.Integer, nullable=False)  
    # Rating for the place, expected to be an integer, cannot be null (typically 0-5 scale)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)  
    # Foreign key linking to the 'places' table, specifying the place being reviewed, cannot be null

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  
    # Foreign key linking to the 'users' table, specifying the user who wrote the review, cannot be null

    place = db.relationship('Place', back_populates='reviews')  
    # Relationship to the Place model, ensures access to all reviews associated with a place

    user = db.relationship('User', back_populates='reviews')  
    # Relationship to the User model, ensures access to all reviews written by a user
