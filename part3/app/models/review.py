from app import db
from models.base_model import BaseModel

class Review(BaseModel, db.Model):
    __tablename__ = 'review'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('place.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='uq_user_place_review'),
    )

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place):
        if isinstance(place, Place):
            self._place = place
            self.save()
        else:
            raise ValueError ("Place do not exist")

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if isinstance(user, User):
            self._user = user
            self.save()
        else:
            raise ValueError ("User do not exist")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if (rating > 0 and rating < 6):       
            self._rating = rating
            self.save()
        else:
            raise ValueError ("rating must be between 1 and 5")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if (len(text) > 0):       
            self._text = text
            self.save()
        else:
            raise ValueError ("the text must not be empty")

    def to_dict(self):
        return {
            'id': self.id,
            'place': self.place.id,
            'user': self.user.id,
            'rating': self.rating,
            'text': self.text
        }
