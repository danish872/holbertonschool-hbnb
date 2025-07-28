import uuid
from datetime import datetime
from app.models.__init__ import db
from sqlalchemy.orm import validates

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be at most 50 characters long.")
        self.name = name
        # id, created_at and updated_at will be handled by default parameters

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Amenity name cannot be empty.")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters long.")
        return name

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
                "id": self.id,
                "name": self.name,
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None
                }

