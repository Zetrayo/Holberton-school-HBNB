from extensions import bcrypt, db
from .baseclass import BaseModel

class User(BaseModel):
    """Represents a user, inherited from BaseModel."""
    
    __tablename__ = 'users'  # Name of the table in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    # Primary key for the user, auto-incremented in the database

    first_name = db.Column(db.String(50), nullable=False)  
    # First name of the user, cannot be null

    last_name = db.Column(db.String(50), nullable=False)  
    # Last name of the user, cannot be null

    email = db.Column(db.String(120), nullable=False, unique=True)  
    # Email of the user, cannot be null and must be unique

    password = db.Column(db.String(128), nullable=False)  
    # Password of the user (hashed), cannot be null

    is_admin = db.Column(db.Boolean, default=False)  
    # Boolean indicating if the user has admin rights, defaults to False

    places = db.relationship('Place', back_populates='user')  
    # Relationship to the Place model, allows access to all places created by the user

    reviews = db.relationship('Review', back_populates='user')  
    # Relationship to the Review model, allows access to all reviews written by the user

    @staticmethod
    def hash_password(password):
        """Hashes the password before storing it in the database."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the stored hashed password."""
        return bcrypt.check_password_hash(self.password, password)
