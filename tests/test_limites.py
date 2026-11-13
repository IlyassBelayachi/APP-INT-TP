"""Tests aux limites du contrat d'entrée (TP4, étape B).

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")

ETIQUETTES = {"POSITIVE", "NEGATIVE", "INDETERMINE"}


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


def poster(client, corps: bytes):
    return client.post("/predict", content=corps, headers={"Content-Type": "application/json"})


def verifier_refus_standard(reponse) -> None:
    """B.2 : un 422 porte la liste d'erreurs standard de FastAPI (objets loc, msg, type)."""
    detail = reponse.json()["detail"]
    assert isinstance(detail, list) and detail, f"detail n'est pas une liste : {detail!r}"
    for erreur in detail:
        assert {"loc", "msg", "type"} <= set(erreur), f"erreur sans loc/msg/type : {erreur!r}"


def verifier_reponse_valide(reponse) -> None:
    corps = reponse.json()
    assert corps["label"] in ETIQUETTES
    assert 0.0 <= corps["score"] <= 1.0


# Étape B.1 : huit cas, un seul test paramétré.
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="texte-d-espaces"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="champ-d-un-autre-type"),
    pytest.param(b"pas du json", 422, id="corps-non-json"),
    # B.6 : si hypothesis trouve un contre-exemple, ajoutez-le ici, par exemple :
    # pytest.param(en_json({"text": "\x85"}), 422, id="blanc-unicode-x85"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = poster(client, corps)
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        verifier_refus_standard(reponse)  # B.2
    else:
        verifier_reponse_valide(reponse)


# Étape B.5 : deux propriétés. « Blanc » = ce que str.strip() retire, comme predict() et le schéma.
BLANCS = [c for c in map(chr, range(0x110000)) if c.isspace()]


@settings(deadline=None)  # le premier appel peut être plus lent que les autres
@given(st.text(min_size=1, max_size=2000).filter(lambda s: s.strip()))
def test_propriete_texte_non_blanc_accepte(client, texte):
    reponse = poster(client, en_json({"text": texte}))
    assert reponse.status_code == 200
    verifier_reponse_valide(reponse)


@settings(deadline=None)
@given(st.text(alphabet=BLANCS, min_size=1, max_size=2000))
def test_propriete_texte_de_blancs_refuse(client, texte):
    reponse = poster(client, en_json({"text": texte}))
    assert reponse.status_code == 422
    verifier_refus_standard(reponse)
