import pytest
import requests
import uuid
from .utils import generate_unique_email

BASE_URL = "http://127.0.0.1:5000/api/v1"


@pytest.fixture
def create_test_user():
    """Fixture pour créer un utilisateur de test"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": generate_unique_email(),
        "password": "Password123!"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)

    assert response.status_code == 201, f"Failed to create test user: {response.text}"

    user = response.json()
    yield user

@pytest.fixture
def create_test_amenity():
    """Fixture pour créer un équipement de test"""
    amenity_data = {
        "name": f"Test Amenity {uuid.uuid4().hex[:8]}",
        "description": "An amenity for testing purposes"
    }
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)

    assert response.status_code == 201, f"Failed to create test amenity: {response.text}"

    amenity = response.json()
    yield amenity


@pytest.fixture
def create_test_place(create_test_user):
    """Fixture pour créer un lieu de test"""
    place_data = {
        "title": "Test Place",
        "description": "A place for testing purposes",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": create_test_user["id"]
    }
    response = requests.post(f"{BASE_URL}/places/", json=place_data)

    assert response.status_code in [200, 201], f"Failed to create test place: {response.text}"

    place = response.json()
    if "id" not in place and "place_id" in place:
        place["id"] = place["place_id"]

    yield place

@pytest.fixture
def create_test_review(create_test_user, create_test_place):
    """Fixture pour créer un avis de test"""
    review_data = {
        "user_id": create_test_user["id"],
        "place_id": create_test_place["id"],
        "rating": 5,
        "comment": "Great place for testing!"
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data)

    assert response.status_code in [200, 201], f"Failed to create test review: {response.text}"

    review = response.json()
    if "id" not in review and "review_id" in review:
        review["id"] = review["review_id"]

    yield review
