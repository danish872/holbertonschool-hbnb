#!/usr/bin/python3

from datetime import datetime
from app.models.base_model import BaseModel
from .place import Place
from .user import User

class Review(BaseModel):
    __slots__ = ('_place', '_user', '_rating', '_comment', '_created_at', '_updated_at')

    def __init__(self, place_id: str, user_id: str, rating: int, comment: str):
        """Initialize a new Review instance."""
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self._created_at: datetime = datetime.utcnow()
        self._updated_at: datetime = self._created_at

    def _validate_str(self, value: str, field: str, max_length: int = None):
        """Validate that value is a non-empty string with an optional max length."""
        if not isinstance(value, str) or not value:
            raise TypeError(f'{field} must be a non-empty string')
        if max_length and len(value) > max_length:
            raise ValueError(f'{field} must be {max_length} characters or less')

    def _validate_int(self, value: int, field: str, min_val: int = None, max_val: int = None):
        """Validate that value is an integer within an optional range."""
        if not isinstance(value, int):
            raise TypeError(f'{field} must be an integer')
        if min_val is not None and value < min_val:
            raise ValueError(f'{field} must be at least {min_val}')
        if max_val is not None and value > max_val:
            raise ValueError(f'{field} must be at most {max_val}')

    def _validate_instance(self, value, expected_type, field: str):
        """Validate that value is an instance of the expected class."""
        if not isinstance(value, expected_type):
            raise TypeError(f'{field} must be an instance of {expected_type.__name__}')

    @property
    def place(self) -> Place:
        return self._place

    @place.setter
    def place(self, value: Place):
        self._validate_instance(value, Place, 'place')
        self._place = value
        self._updated_at = datetime.utcnow()

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, value: User):
        self._validate_instance(value, User, 'user')
        self._user = value
        self._updated_at = datetime.utcnow()

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int):
        self._validate_int(value, 'rating', min_val=0, max_val=5)
        self._rating = value
        self._updated_at = datetime.utcnow()

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._validate_str(value, 'comment', max_length=500)
        self._comment = value
        self._updated_at = datetime.utcnow()

    def create_review(self) -> None:
        """Create a new review (logic to persist it in the database can be added)."""
        self._created_at = datetime.utcnow()
        self._updated_at = self._created_at
        self.save()

    def update_review(self, **kwargs) -> None:
        """Update review attributes dynamically."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._updated_at = datetime.utcnow()
        self.save()

    def delete_review(self) -> None:
        """Delete the review (logic to remove it from the database can be added)."""
        del self

    def to_dict(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment
        }
