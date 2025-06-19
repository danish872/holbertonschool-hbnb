import requests
import pytest
import uuid


class TestReviews:
    
    def test_create_review_success(self, create_test_user, create_test_place):
        """Test de création d'un avis avec succès"""
        review_data = {
            "user_id": create_test_user["id"],
            "place_id": create_test_place["id"],
            "rating": 4,
            "comment": "A good place to stay!"
        }
        response = requests.post(f"{BASE_URL}/reviews/", json=review_data)

        assert response.status_code in [200, 201], f"Response: {response.text}"

        review = response.json()

        review_id = review.get("id") or review.get("review_id")
        assert review_id is not None, "No ID found in review response"

        user_id = review.get("user_id")
        place_id = review.get("place_id")
        rating = review.get("rating")
        comment = review.get("comment") or review.get("text")

        assert user_id == review_data["user_id"]
        assert place_id == review_data["place_id"]
        assert rating == review_data["rating"]
        assert comment == review_data["comment"]

    def test_create_review_missing_fields(self, create_test_user, create_test_place):
        """Test de création d'un avis avec des champs manquants"""
        review_data = {
            "user_id": create_test_user["id"],
            "place_id": create_test_place["id"]
            
        }
        response = requests.post(f"{BASE_URL}/reviews/", json=review_data)

        assert response.status_code == 400, f"Response: {response.text}"

        data = response.json()
        assert "message" in data or "error" in data

    def test_create_review_invalid_rating(self, create_test_user, create_test_place):
        """Test de création d'un avis avec une note invalide"""
        review_data = {
            "user_id": create_test_user["id"],
            "place_id": create_test_place["id"],
            "rating": 10,  # Devrait être entre 0 et 5
            "comment": "Invalid rating test"
        }
        response = requests.post(f"{BASE_URL}/reviews/", json=review_data)

        assert response.status_code == 400, f"Response: {response.text}"

        data = response.json()
        assert "message" in data or "error" in data

    def test_get_all_reviews(self):
        """Test pour récupérer tous les avis"""
        response = requests.get(f"{BASE_URL}/reviews/")

        assert response.status_code == 200, f"Response: {response.text}"

        data = response.json()
        assert "reviews" in data
        assert isinstance(data["reviews"], list)

    def test_get_review_by_id(self, create_test_review):
        """Test pour récupérer un avis par son ID"""
        review_id = create_test_review["id"]
        response = requests.get(f"{BASE_URL}/reviews/{review_id}")

        assert response.status_code == 200, f"Response: {response.text}"

        review = response.json()

        response_id = review.get("id") or review.get("review_id")
        assert response_id == review_id

        assert review["user_id"] == create_test_review["user_id"]
        assert review["place_id"] == create_test_review["place_id"]
        assert review["rating"] == create_test_review["rating"]
        comment = review.get("comment") or review.get("text")
        expected_comment = create_test_review.get("comment") or create_test_review.get("text")
        assert comment == expected_comment

    def test_get_reviews_by_place(self, create_test_place, create_test_review):
        """Test pour récupérer tous les avis d'un lieu spécifique"""
        place_id = create_test_place["id"]

        if create_test_review["place_id"] != place_id:
            pytest.skip("Test review does not match test place - can't test get_reviews_by_place")

        response = requests.get(f"{BASE_URL}/reviews/places/{place_id}")

        assert response.status_code == 200, f"Response: {response.text}"

        reviews_data = response.json()
        if isinstance(reviews_data, dict) and "reviews" in reviews_data:
            reviews = reviews_data["reviews"]
        else:
            reviews = reviews_data

        assert isinstance(reviews, list)

        if reviews:
            review_ids = []
            for review in reviews:
                review_id = review.get("id") or review.get("review_id")
                if review_id:
                    review_ids.append(review_id)

            review_id = create_test_review["id"]
            assert review_id in review_ids, f"Review ID {review_id} not found in {review_ids}"

    def test_get_review_not_found(self):
        """Test pour récupérer un avis qui n'existe pas"""
        nonexistent_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/reviews/{nonexistent_id}")

        assert response.status_code == 404, f"Response: {response.text}"

        data = response.json()
        assert "error" in data

    def test_update_review(self, create_test_review):
        """Test pour mettre à jour un avis"""
        review_id = create_test_review["id"]

        comment_field = "comment"
        if "text" in create_test_review:
            comment_field = "text"

        update_data = {
            "user_id": create_test_review["user_id"],
            "place_id": create_test_review["place_id"],
            "rating": 3,
            comment_field: "Updated review comment"
        }

        response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data)

        assert response.status_code == 200, f"Response: {response.text}"

        updated_review = response.json()

        response_id = updated_review.get("id") or updated_review.get("review_id")
        assert response_id == review_id

        assert updated_review["rating"] == update_data["rating"]

        actual_comment = updated_review.get("text") or updated_review.get("comment")
        assert actual_comment == update_data[comment_field]
