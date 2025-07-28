from app import db
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

# Table d'association many-to-many entre Place et Amenity
place_amenity = db.Table('place_amenity',
        db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
        db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
        )

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            backref=db.backref('places', lazy='dynamic')
            )

    @validates("title")
    def validate_title(self, key, title):
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters.")
        return title

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price must be a positive number.")
        return price

    @validates("latitude")
    def validate_latitude(self, key, latitude):
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    @validates("longitude")
    def validate_longitude(self, key, longitude):
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return longitude

    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "owner_id": self.owner_id,
                "amenities": [amenity.to_dict() for amenity in self.amenities],
                "reviews": [review.to_dict() for review in self.reviews],
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }

