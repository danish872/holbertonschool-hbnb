from app import db, bcrypt
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
import re

class User(BaseModel, db.Model):
    __tablename__ = 'user'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='author', lazy=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """Hashes the password before storing it."""
        self._password = app.bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return app.bcrypt.check_password_hash(self.password, password)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
            self._email = email
            self.save()
        else:
            raise ValueError ("Email is not conforme to standar")
    
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if (len(first_name) > 50):
            raise ValueError ("First name to long")
        elif (first_name == ""):
            raise ValueError ("First name mustn't be empty")
        else:
            self._first_name = first_name
            self.save()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if(len(last_name) > 50):
            raise ValueError ("Last name to long")
        elif (last_name == ""):
            raise ValueError ("Last name mustn't be empty")
        else:
            self._last_name = last_name
            self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
