#!/usr/bin/python3
from extensions import db

place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True),
    extend_existing=True  # Only if you need to redefine it
)

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    places = db.relationship('Place', secondary=place_amenities, back_populates='amenities')
