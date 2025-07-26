from app import db, bcrypt
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel
import re
from sqlalchemy import inspect

class User(BaseModel):
    __tablename__ = 'user'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
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
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
            return email
        else:
            raise ValueError ("Email is not conforme to standar")
    
    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if (len(first_name) > 50):
            raise ValueError ("First name to long")
        elif (first_name == ""):
            raise ValueError ("First name mustn't be empty")
        else:
            return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if(len(last_name) > 50):
            raise ValueError ("Last name to long")
        elif (last_name == ""):
            raise ValueError ("Last name mustn't be empty")
        else:
            return last_name

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

def create_first_admin():
    inspector = inspect(db.engine)
    if inspector.has_table("user"):
        admin_email = "admin@root.com"
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(
                first_name="Admin",
                last_name="root",
                email=admin_email,
                is_admin=True
            )
            admin.hash_password("jsp1234")
            db.session.add(admin)
            db.session.commit()
