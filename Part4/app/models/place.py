#!/usr/bin/python3
from extensions import db
from sqlalchemy.orm import relationship
from .baseclass import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place')
    amenities = db.relationship('Amenity', secondary='place_amenities', back_populates='places')
