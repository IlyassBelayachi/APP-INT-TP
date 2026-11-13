# Semaine 5 : l'interface, notes du binôme

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface Streamlit communique avec le backend FastAPI à travers des requêtes HTTP vers l'endpoint `/predict`. Cette séparation permet de respecter l'architecture client-serveur : l'interface s'occupe uniquement de l'affichage et de l'interaction avec l'utilisateur, tandis que l'API gère les prédictions et le chargement du modèle. Cela facilite la maintenance et permet de faire évoluer l'interface ou le modèle indépendamment.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Lorsque le modèle n'a pas suffisamment confiance dans sa prédiction, l'interface affiche le verdict `INDETERMINE` avec le message : « Je ne sais pas : à faire vérifier par un humain ». Cette approche est préférable à un verdict forcé, car elle évite de présenter une classification incertaine comme une décision fiable. Elle permet donc de signaler les cas ambigus et de demander une vérification humaine.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Lorsque l'API est indisponible, l'interface affiche un message explicite indiquant que l'API est injoignable, au lieu de provoquer une erreur incompréhensible pour l'utilisateur. Dans le fichier CSV de six avis, un seul avis reçoit le verdict `INDETERMINE` et doit donc être vérifié par un humain. Les cinq autres avis sont classés automatiquement : trois positifs et deux négatifs.