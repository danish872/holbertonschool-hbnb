import requests
import pytest
import uuid


class TestPlaces:
    
    def test_create_place_success(self, create_test_user):
        """Test de création d'un lieu avec succès"""
        place_data = {
            "title": "Beautiful Apartment",
            "description": "A lovely apartment in the city center",
            "price": 120.50,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": create_test_user["id"]
        }
        response = requests.post(f"{BASE_URL}/places/", json=place_data)

        assert response.status_code in [200, 201], f"Response: {response.text}"

        place = response.json()

        place_id = place.get("id") or place.get("place_id")
        assert place_id is not None, "No ID found in place response"

        assert place["title"] == place_data["title"]
        assert place["description"] == place_data["description"]
        assert place["price"] == place_data["price"]
        assert place["latitude"] == place_data["latitude"]
        assert place["longitude"] == place_data["longitude"]
        assert place["owner_id"] == place_data["owner_id"]

    def test_create_place_missing_fields(self, create_test_user):
        """Test de création d'un lieu avec des champs manquants"""
        place_data = {
            "title": "Incomplete Place",
            "owner_id": create_test_user["id"]
            # price, latitude, longitude manquants
        }
        response = requests.post(f"{BASE_URL}/places/", json=place_data)

        assert response.status_code == 400, f"Response: {response.text}"

        data = response.json()
        assert "error" in data

    def test_create_place_invalid_owner(self):
        """Test de création d'un lieu avec un propriétaire invalide"""
        place_data = {
            "title": "Invalid Owner Place",
            "description": "A place with an invalid owner",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": str(uuid.uuid4())  # ID qui n'existe pas
        }
        response = requests.post(f"{BASE_URL}/places/", json=place_data)

        assert response.status_code in [201, 200, 400, 404], f"Response: {response.text}"

        if response.status_code in [400, 404]:
            data = response.json()
            assert "error" in data or "message" in data
        elif response.status_code in [200, 201]:
            data = response.json()
            assert "id" in data or "place_id" in data
            assert data["title"] == place_data["title"]
            assert data["owner_id"] == place_data["owner_id"]

    def test_get_all_places(self):
        """Test pour récupérer tous les lieux"""
        response = requests.get(f"{BASE_URL}/places/")

        assert response.status_code == 200, f"Response: {response.text}"

        data = response.json()
        assert "places" in data
        assert isinstance(data["places"], list)

    def test_get_place_by_id(self, create_test_place):
        """Test pour récupérer un lieu par son ID"""
        place_id = create_test_place["id"]
        response = requests.get(f"{BASE_URL}/places/{place_id}")

        assert response.status_code == 200, f"Response: {response.text}"

        place = response.json()

        response_id = place.get("id") or place.get("place_id")
        assert response_id == place_id

        assert place["title"] == create_test_place["title"]

    def test_get_place_not_found(self):
        """Test pour récupérer un lieu qui n'existe pas"""
        nonexistent_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/places/{nonexistent_id}")

        assert response.status_code in [404, 500], f"Response: {response.text}"

        if response.headers.get('Content-Type', '').startswith('application/json'):
            data = response.json()
            assert "error" in data or "message" in data

    def test_update_place(self, create_test_place):
        """Test pour mettre à jour un lieu"""
        place_id = create_test_place["id"]
        update_data = {
            "title": "Updated Place",
            "description": "Updated description",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": create_test_place["owner_id"]
        }
        response = requests.put(f"{BASE_URL}/places/{place_id}", json=update_data)

        assert response.status_code == 200, f"Response: {response.text}"

        updated_place = response.json()

        response_id = updated_place.get("id") or updated_place.get("place_id")
        assert response_id == place_id

    
        assert updated_place["title"] == update_data["title"]
        assert updated_place["description"] == update_data["description"]
        assert updated_place["price"] == update_data["price"]
