import uuid
from datetime import datetime
from sqlalchemy.orm import validates
from app.models.__init__ import db


class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be at most 50 characters long.")
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Amenity name is required and must be at most 50 characters long.")
        return value

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
                "id": self.id,
                "name": self.name,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }

