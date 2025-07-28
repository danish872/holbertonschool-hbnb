from app import db, bcrypt
from sqlalchemy.orm import relationship, validates
from sqlalchemy import inspect
from app.models.base_model import BaseModel
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='author', lazy=True)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @validates("email")
    def validate_email(self, key, email):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$'
        if re.fullmatch(pattern, email):
            return email
        raise ValueError("Invalid email format.")

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if not first_name.strip():
            raise ValueError("First name must not be empty.")
        if len(first_name) > 50:
            raise ValueError("First name is too long.")
        return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if not last_name.strip():
            raise ValueError("Last name must not be empty.")
        if len(last_name) > 50:
            raise ValueError("Last name is too long.")
        return last_name

    def to_dict(self):
        return {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin
                }

def create_first_admin():
    inspector = inspect(db.engine)
    if inspector.has_table("users"):
        admin_email = "admin@root.com"
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(
                    first_name="Admin",
                    last_name="Root",
                    email=admin_email,
                    is_admin=True
                    )
            admin.hash_password("jsp1234")
            db.session.add(admin)
            db.session.commit()

