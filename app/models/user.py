from app.models.__init__ import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if(len(first_name) > 50):
            raise ValueError ("First name to long")
        else:
            self._first_name = first_name
        if(len(last_name) > 50):
            raise ValueError ("Last name to long")
        else:
            self._last_name = last_name
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
            self._email = email
        else:
            raise ValueError ("Email is not conforme to standard")
        self.is_admin = is_admin
        self.places = []

    def add_place(self, place):
        self.places.append(place)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
            self._email = email
        else:
            raise ValueError ("Email is not conforme to standar")
    
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if(len(first_name) > 50):
            raise ValueError ("First name to long")
        else:
            self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if(len(last_name) > 50):
            raise ValueError ("Last name to long")
        else:
            self._last_name = last_name

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
