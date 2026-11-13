# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.
> Les passages entre crochets [À RECOPIER] sont à remplir avec vos mesures de l'étape A.

## 1. Couverture

- Avant (étape A) : 
- Pour chacune, le comportement qu'aucun test ne vérifiait :
  - la réponse 503 quand le modèle n'est pas chargé ;
  - la réponse 500 quand le modèle tombe en panne ;
  - le lancement direct du fichier (`if __name__ == "__main__":`).
- Après (étape D) : 97,37 % (`api/main.py` 95 %, `api/model.py` 100 %, `api/schemas.py` 100 %). Seules les lignes 83 à 85 de `main.py` restent non couvertes : c'est le bloc de lancement direct, que pytest n'exécute pas.
- Lignes exclues de la mesure : aucune. Aucun `# pragma: no cover` n'a été nécessaire pour atteindre le seuil de 95 %.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| `{"text": "   "}` reçoit un 422 dont `detail` est une chaîne (`"texte vide"`), alors que les autres refus donnent une liste ; hypothesis trouve `'\x85'`, que `str.strip()` retire mais que le schéma laisse passer. Le schéma et `predict()` avaient deux définitions de « vide ». | `test_frontieres_du_contrat[texte-d-espaces]` et `test_propriete_texte_de_blancs_refuse` | `field_validator` dans `api/schemas.py`, même règle que `predict()` (`str.strip()`) |
| Un texte de mots inventés reçoit `NEGATIVE` à 0,5162 : aucun mot n'est dans le vocabulaire, le vecteur TF-IDF est nul et il ne reste que l'ordonnée à l'origine de la régression logistique | Essai manuel dans `/docs` (contrôle T24) | `SEUIL_ABSTENTION = 0.60` et verdict `INDETERMINE` dans `api/model.py` |
| Une panne du modèle (`ValueError("bug interne")`) reçoit un 422 qui expose le message interne au client | `test_panne_du_modele_repond_500_sans_message_interne[ValueError]` | Suppression de la conversion de `ValueError` en 422 dans `api/main.py` : toute panne répond 500 |
| Le contrat des étiquettes n'était pas vérifié : `predict()` renvoyait un `dict` sans type, donc des `Any` que mypy ne contrôle pas | Relecture de `mypy api` (muet sur les étiquettes) ; `test_classes_inattendues_refusent_de_demarrer` | `TypedDict` et `Literal`, table `CORRESPONDANCE` explicite à la place de `.upper()`, vérification des classes du modèle au démarrage |

## 3. Seuil d'abstention

Courbe mesurée avec `python src/courbe_seuil.py` sur le jeu de test du TP2 (58 avis) :

| Seuil | Répond à | Part | Exactitude | Erreurs | Vers un humain |
| --- | --- | --- | --- | --- | --- |
| 0,50 | 58 | 100 % | 0,879 | 7 | 0 |
| 0,60 | 42 | 72 % | 0,952 | 2 | 16 |
| 0,70 | 37 | 64 % | 1,000 | 0 | 21 |

- Seuil retenu : **0,60**. Part des avis envoyés à un humain : 16 sur 58, soit 28 %.
- Justification : 5 des 7 erreurs du seuil 0,50 sont évitées, et l'exactitude sur les avis traités passe de 0,879 à 0,952. Le seuil 0,65 n'évite qu'une erreur de plus (1 avis de plus vers un humain) ; au-delà de 0,70 le modèle abandonne plus d'un tiers des avis sans que l'exactitude progresse.
- Limites : le jeu de test ne compte que 58 avis, donc un écart d'un ou deux avis pèse beaucoup ; le seuil est choisi sur ce même jeu, l'exactitude annoncée est donc un peu optimiste.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) sur 20 avis : **9 justes, 8 abstentions, 3 erreurs franches déclarées** (aucune erreur franche non déclarée).
- Les trois erreurs franches sont des avis négatifs classés `POSITIVE` (confiances de 0,63 à 0,70), tous trois à cause d'une négation (« non conforme », « pas satisfait », « ne recommande à personne »). Ils restent dans le jeu, déclarés dans `erreur_connue`, et apparaissent en `xfailed`.
- Ce que ces chiffres disent du modèle : sur les 12 avis où il répond, 9 sont justes (75 %), contre 0,952 attendu à 0,60 sur le jeu de test : le jeu d'or, plus varié, est plus exigeant. 40 % des avis partent vers un humain, contre 28 % sur le jeu de test. Surtout, les trois erreurs ont une confiance **au-dessus du seuil** : l'abstention ne protège pas contre elles. Le modèle en sac de mots lit « conforme », « satisfait » ou « recommande » sans comprendre la négation, et une confiance élevée ne garantit pas qu'il ait raison.

## 5. Outils statiques

- Remarques au départ : ruff [À RECOPIER : nombre mesuré à l'étape A], mypy [À RECOPIER : résultat de `mypy api`, « Success » attendu].
- Parmi les défauts de la partie 2, ruff n'en avait signalé aucun directement : sa seule remarque liée à ces défauts était `B904` (le `raise` du 500 sans `from None`), qui concerne le style de l'exception, pas la panne qui répondait 422 avec le message interne. mypy ne signalait rien du tout, car un `dict` sans type ne transporte que des `Any`.
- Conclusion : les outils statiques voient le style, les imports inutiles et les types déclarés, mais pas le comportement. Les défauts du contrat d'entrée, de l'abstention et des pannes n'ont été trouvés que par les tests (hypothesis, tests d'intégration, jeu d'or). mypy ne devient utile sur les étiquettes qu'une fois les types précisés.
