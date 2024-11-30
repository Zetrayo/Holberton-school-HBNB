import uuid
from datetime import datetime
from extensions import db

class BaseModel(db.Model):
    """Base model for other database models to inherit from.
    
    This model provides common fields like id, created_at, and updated_at
    for all models that inherit from it.
    """
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class directly

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  
    # Unique identifier for the record, generated as a UUID string (36 characters long)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    # Timestamp for when the record was created, defaulting to the current UTC time

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
    # Timestamp for when the record was last updated, automatically set to the current UTC time on update
