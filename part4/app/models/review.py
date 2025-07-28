from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (
            db.UniqueConstraint('user_id', 'place_id', name='uq_user_place_review'),
            )

    @validates("rating")
    def validate_rating(self, key, rating):
        if 1 <= int(rating) <= 5:
            return rating
        raise ValueError("Rating must be between 1 and 5.")

    @validates("text")
    def validate_text(self, key, text):
        if text and text.strip():
            return text
        raise ValueError("Review text must not be empty.")

    def to_dict(self):
        return {
                "id": self.id,
                "text": self.text,
                "rating": self.rating,
                "place_id": self.place_id,
                "user_id": self.user_id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
                }

