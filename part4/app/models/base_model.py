import uuid
from datetime import datetime
from app import db
from abc import ABC, abstractmethod


class BaseModel(db.Model, ABC):
    __abstract__ = True  # Ne crée pas de table pour ce modèle

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Met à jour la date de modification et enregistre l'objet en base de données"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Met à jour les attributs de l'objet à partir d'un dictionnaire"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    @abstractmethod
    def to_dict(self):
        """Méthode abstraite à implémenter dans les sous-classes pour convertir l'objet en dictionnaire"""
        pass

