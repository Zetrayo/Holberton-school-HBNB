#!/usr/bin/python3
from extensions import db
from .baseclass import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
