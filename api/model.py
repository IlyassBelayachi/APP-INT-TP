"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path
from typing import TypedDict

from api.schemas import Etiquette

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import charger_modele  # noqa: E402  (src/ doit être dans sys.path avant l'import)
from predict import predict as _predict  # noqa: E402

# TP4, étape C : sous cette confiance, le modèle ne tranche pas et l'avis part vers un humain.
# Valeur choisie d'après la courbe de src/courbe_seuil.py : 28 % des avis de test envoyés
# à un humain, 5 des 7 erreurs du seuil 0,50 évitées.
SEUIL_ABSTENTION = 0.60
INDETERMINE: Etiquette = "INDETERMINE"

# TP4, étape E : correspondance explicite entre les classes du modèle et les étiquettes du contrat.
CORRESPONDANCE: dict[str, Etiquette] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class Resultat(TypedDict):
    """Retour de SentimentClassifier.predict() : le contrat de l'API."""

    label: Etiquette
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()  # échoue immédiatement si le joblib manque
        inconnues = set(pipeline.classes_) - set(CORRESPONDANCE)
        if inconnues:  # on ne démarre pas avec un modèle dont les classes sortent du contrat
            raise RuntimeError(f"classes du modèle absentes de la correspondance : {sorted(inconnues)}")

    def predict(self, text: str) -> Resultat:
        """Renvoie {'label': POSITIVE|NEGATIVE|INDETERMINE, 'score': float, 'text': aperçu}.

        Sous SEUIL_ABSTENTION, l'étiquette devient INDETERMINE ; le score reste renvoyé.
        """
        r = _predict(text)  # lève ValueError si le texte est vide
        label = CORRESPONDANCE[r["label"]] if r["score"] >= SEUIL_ABSTENTION else INDETERMINE
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
