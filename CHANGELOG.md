# Journal des versions

Le numéro de version suit les TP : 0.N.0 à la fin du TP N. Chaque version publiée porte une étiquette Git `v0.N.0`.

## 0.6.0 (TP6) : le paquet

- Pour celui qui installe : le dépôt est un paquet Python (`pip install` d'une roue `sentiment_app-0.6.0`), avec la commande `sentiment` (`--version`, `predict`, `serve`, `ui`) ; le modèle n'est pas dans la roue, on l'indique par `SENTIMENT_MODELE`.
- Pour celui qui développe : `predict.py` est dans `sentiment_app/` ; `api/model.py` l'importe sans toucher à `sys.path` ; `src/predict.py` reste en compatibilité ; `pip install -e .` pour travailler.
- Pour la CI : scikit-learn épinglé en 1.5, pytest en 8.3, et une étape qui construit la roue, l'installe hors du dépôt et l'essaie.

## 0.5.0 (TP5) : l'interface

- Page Streamlit : un avis, ou un fichier d'avis ; le client HTTP traduit chaque réponse de l'API.

## 0.4.0 (TP4) : tests et qualité

- Contrat d'entrée testé, abstention `INDETERMINE`, jeu d'or, tests d'intégration, contrat typé, ruff, mypy, pre-commit.

## 0.3.0 (TP3) : l'API

- FastAPI : `/health`, `/predict`, contrat Pydantic ; la CI entraîne le modèle avant les tests.

## 0.2.0 (TP2) : le modèle

- TF-IDF et régression logistique ; les métriques sont versionnées, le modèle ne l'est pas.

## 0.1.0 (TP1) : le cadrage

- Environnement Python 3.11, structure du dépôt, trois fiches de cadrage, dépôt GitHub à deux auteurs.
