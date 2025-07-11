from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'review'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('place.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='uq_user_place_review'),
    )

    @validates("rating")
    def validate_rating(self, key, rating):
        if (rating > 0 and rating < 6):
            return rating
        else:
            raise ValueError ("rating must be between 1 and 5")

    @validates("text")
    def validate_text(self, key, text):
        if (len(text) > 0 and text != ""):       
            return text
        else:
            raise ValueError ("the text must not be empty")

    def to_dict(self):
        return {
            'id': self.id,
            'place': self.place_id,
            'user': self.user_id,
            'rating': self.rating,
            'text': self.text
        }
