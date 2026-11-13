"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
Toute modification d'état passe par monkeypatch, qui restaure l'état à la fin du test.
"""
import importlib
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")

CORPS = {"text": "Livraison rapide, produit conforme, très satisfait"}


class ModeleEnPanne:
    """Faux classifier dont predict() lève l'exception donnée."""

    model_name = "modèle en panne (test)"

    def __init__(self, erreur: Exception) -> None:
        self.erreur = erreur

    def predict(self, text: str) -> dict:
        raise self.erreur


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_de_demarrer(monkeypatch, tmp_path):
    """D.2 : sans fichier modèle, l'API ne démarre pas (le contrôle T20 du TP3, automatique)."""
    from fastapi.testclient import TestClient

    from api.main import app  # l'import de api.model ajoute src/ au chemin de recherche

    predict_tp2 = importlib.import_module("predict")  # module du TP2, dans src/
    monkeypatch.setattr(predict_tp2, "MODELE", tmp_path / "absent.joblib")
    predict_tp2.charger_modele.cache_clear()  # sinon le modèle déjà chargé est réutilisé
    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass


def test_modele_non_charge_repond_503(monkeypatch):
    """D.3 : l'API démarrée, modèle retiré de app.state : 503 sur /health et /predict."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", None)
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json=CORPS).status_code == 503


@pytest.mark.parametrize(
    "erreur",
    [RuntimeError("panne du modèle"), ValueError("bug interne")],
    ids=["RuntimeError", "ValueError"],
)
def test_panne_du_modele_repond_500_sans_message_interne(monkeypatch, erreur):
    """D.4 : quelle que soit l'exception, 500 ; le message interne ne sort pas du serveur."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", ModeleEnPanne(erreur))
        reponse = client.post("/predict", json=CORPS)
    assert reponse.status_code == 500
    assert str(erreur) not in reponse.text
    assert reponse.json()["detail"] == "Erreur interne du serveur"


def test_classes_inattendues_refusent_de_demarrer(monkeypatch):
    """E.3 : un modèle dont les classes sortent de la correspondance empêche le démarrage."""
    import api.model as modele

    class PipelineAvecClasseInconnue:
        classes_ = ["positive", "mitige"]

    monkeypatch.setattr(modele, "charger_modele", lambda: PipelineAvecClasseInconnue())
    with pytest.raises(RuntimeError, match="mitige"):
        modele.SentimentClassifier()
