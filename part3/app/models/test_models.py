import sys
import os
import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class TestUser(unittest.TestCase):
    def test_initialization(self):
        user = User("john_doe", "securepassword", is_admin=False)
        self.assertEqual(user.username, "john_doe")
        self.assertFalse(user.is_admin)

    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            User("", "password")

    def test_invalid_password(self):
        with self.assertRaises(ValueError):
            User("john_doe", "123")

    def test_invalid_admin(self):
        with self.assertRaises(ValueError):
            User("bob_m", "mypassword", is_admin="admin")

class TestPlace(unittest.TestCase):
    def test_initialization(self):
        place = Place("Beautiful Home", "A lovely place", 200, 40.7128, -74.0060, "Owner")
        self.assertEqual(place.title, "Beautiful Home")
        self.assertEqual(place.description, "A lovely place")
        self.assertEqual(place.price, 200)
        self.assertEqual(place.owner, "Owner")
        self.assertEqual(len(place.reviews), 0)
        self.assertEqual(len(place.amenities), 0)

    def test_invalid_title(self):
        with self.assertRaises(ValueError):
            place = Place("", "Description", 100, 10.0, 10.0, "Owner")

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            place = Place("Home", "Description", -100, 10.0, 10.0, "Owner")

    def test_invalid_coordinates(self):
        place = Place("Home", "Description", 100, 10.0, 10.0, "Owner")
        with self.assertRaises(ValueError):
            place.set_coordinates(100, 200)

class TestReview(unittest.TestCase):
    def test_initialization(self):
        user = User("john_doe", "securepassword", is_admin=False)
        place = Place("Home", "Description", 100, 10.0, 10.0, "Owner")
        review = Review("Great place", 5, place, user)
        self.assertEqual(review.text, "Great place")
        self.assertEqual(review.rating, 5)
        self.assertIsInstance(review.id, str)
        self.assertIsNotNone(review.created_at)

    def test_invalid_rating(self):
        user = User("jane_doe", "mypassword", is_admin=False)
        place = Place("Home", "Description", 100, 10.0, 10.0, "Owner")
        with self.assertRaises(ValueError):
            Review("Bad", 6, place, user)

    def test_invalid_place(self):
        user = User("john_doe", "securepassword", is_admin=False)
        with self.assertRaises(ValueError):
            Review("Nice", 5, "Not a Place", user)

    def test_invalid_user(self):
        place = Place("Home", "Description", 100, 10.0, 10.0, "Owner")
        with self.assertRaises(ValueError):
            Review("Nice", 5, place, "Not a User")

if __name__ == '__main__':
    unittest.main()
