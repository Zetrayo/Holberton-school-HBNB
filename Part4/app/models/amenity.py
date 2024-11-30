from extensions import db

# Association table for the many-to-many relationship between Place and Amenity
place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),  # Foreign key to 'places' table
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True),  # Foreign key to 'amenities' table
    extend_existing=True  # Ensures no conflicts if the table is redefined elsewhere
)

class Amenity(db.Model):
    """Represents an amenity (e.g., Pool, WiFi) available for places."""
    __tablename__ = 'amenities'  # Define the name of the table in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the amenity
    name = db.Column(db.String(128), nullable=False)  # Name of the amenity (e.g., 'WiFi', 'Swimming Pool')

    # Relationship with Place model: many-to-many relationship through the 'place_amenities' table
    places = db.relationship(
        'Place', 
        secondary=place_amenities,  # The association table
        back_populates='amenities'  # Back-reference to the 'amenities' field in the Place model
    )
