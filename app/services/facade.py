from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()  # dépôt spécifique aux amenities

    def create_amenity(self, amenity_data):
        # Création d'une instance d'amenity avec les données reçues
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Recherche par ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Récupération de toutes les amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Mise à jour d'une amenity existante
        return self.amenity_repo.update(amenity_id, amenity_data)
