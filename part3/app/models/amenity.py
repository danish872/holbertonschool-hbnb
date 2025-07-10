from app import db
from models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'

    name = db.Column(db.String(255), nullable=False, unique=True)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if(len(name) <= 50):
            self._name = name
            self.save()
        else:
            raise ValueError ("name is too long")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
