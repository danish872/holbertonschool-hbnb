import uuid

def generate_unique_email():
    """Génère un email unique pour les tests"""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

