from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates 

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates("name")
    def validate_name(self, key, name):
        if(len(name) <= 50):
            self.save()
            return name
        raise ValueError ("name is too long")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
