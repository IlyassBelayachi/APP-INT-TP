"""Contrats d'entrée et de sortie de l'API (Pydantic v2)."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# Les trois verdicts du contrat : le même type sert au modèle (api/model.py) et à la réponse.
Etiquette = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class PredictRequest(BaseModel):
    """Requête de prédiction."""
    text: str = Field(..., min_length=1, max_length=2000, description="Texte à classifier",
                      examples=["Livraison rapide, produit conforme, très satisfait"])

    @field_validator("text")
    @classmethod
    def refuser_texte_blanc(cls, v: str) -> str:
        """Refuse un texte vide une fois ses blancs retirés (même règle que predict(), TP2)."""
        if not v.strip():
            raise ValueError("texte vide")
        return v


class PredictResponse(BaseModel):
    """Réponse de prédiction."""
    label: Etiquette = Field(
        ..., description="POSITIVE, NEGATIVE ou INDETERMINE (confiance sous le seuil d'abstention)")
    score: float = Field(..., ge=0, le=1, description="Confiance de la classe prédite")
    text: str = Field(..., description="Aperçu du texte analysé (100 caractères)")


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""
    status: str = Field(..., description="OK si le modèle est chargé")
    model: str = Field(..., description="Nom du modèle servi")


class ErrorResponse(BaseModel):
    """Format standard des erreurs FastAPI."""
    detail: str
