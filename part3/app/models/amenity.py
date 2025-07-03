from app import db
from models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenity'

    name = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
