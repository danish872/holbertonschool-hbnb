from app import db
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

# Association table many-to-many
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('place.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'place'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy='dynamic'))

    @validates("title")
    def validate_title(self, key, title):
        if(len(title) < 101 and title != ""):
            return title
        else:
            raise ValueError ("Title is not conforme to standar")

    @validates("price")
    def validate_price(self, key, price):
        if(price >= 0):
            return price
        else:
            raise ValueError ("price must be positif")
    
    @validates("latitude")
    def validate_latitude(self, key, latitude):
        if(latitude >= -90 and latitude <= 90):
            return latitude
        else:
            raise ValueError ("latitude must be within the range of -90.0 to 90.0")

    @validates("longitude")
    def validate_longitude(self, key, longitude):
        if(longitude >= -180 and longitude <= 180):
            return longitude
        else:
            raise ValueError ("longitude must be within the range of -180.0 to 180.0")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict(),
            "amenities": [element.to_dict() for element in self.amenities],
            "reviews": [element.to_dict() for element in self.reviews]
        }
