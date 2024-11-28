# app/models/base_model.py
import uuid
from datetime import datetime
from extensions import db

class BaseModel(db.Model):
    __abstract__ = True  # Empêche SQLAlchemy de créer une table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
