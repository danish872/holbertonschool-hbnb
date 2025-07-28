import uuid
from datetime import datetime
from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __init__(self, first_name='', last_name='', email='', password='', is_admin=False):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.hash_password(password)

    def hash_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @validates('email')
    def validate_email(self, key, email):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$'
        if not re.match(pattern, email):
            raise ValueError("Email is not valid")
        return email

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name or len(first_name) > 50:
            raise ValueError("First name must be 1-50 characters long")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name must be 1-50 characters long")
        return last_name

    def to_dict(self):
        return {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin,
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                }

