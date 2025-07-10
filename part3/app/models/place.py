from app import db
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

# Association table many-to-many
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('place.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenity.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    __tablename__ = 'place'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy='dynamic'))

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        if (isinstance(owner, User)):
            self._owner = owner
            self.save()
        else:
            raise ValueError ("owner not found")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if(len(title) < 101):
            self._title = title
            self.save()
        else:
            raise ValueError ("Title is not conforme to standar")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if(price >= 0):
            self._price = price
            self.save()
        else:
            raise ValueError ("price must be positif")
    
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if(latitude >= -90 and latitude <= 90):
            self._latitude = latitude
            self.save()
        else:
            raise ValueError ("latitude must be within the range of -90.0 to 90.0")

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if(longitude >= -180 and longitude <= 180):
            self._longitude = longitude
            self.save()
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
            "amenities": [element.to_dict() for element in self.amenities]
        }
