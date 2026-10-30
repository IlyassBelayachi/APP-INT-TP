# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Classer automatiquement les avis clients d'un site e-commerce pour faire remonter en priorité les avis négatifs au service client.

## Utilisateur final (obligatoire)

Les agents du service client, qui traitent en premier les avis signalés comme négatifs, et le responsable qualité qui suit les problèmes récurrents.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Le site dispose de milliers d'avis que l'on peut étiqueter, par exemple grâce à la note en étoiles puis une vérification manuelle d'un échantillon, ce qui permet d'entraîner un classifieur supervisé (a). Le volume est élevé : un petit modèle entraîné coûte très peu par requête, contrairement à un modèle génératif appelé pour chaque avis (c). Un avis négatif non détecté laisse un client mécontent sans réponse, donc l'erreur est mesurable et doit être contrôlée par un seuil de rappel sur la classe négative (d).

## Données nécessaires et leur origine (obligatoire)

Les avis clients du site, avec leur note en étoiles, qui servent d'étiquette de départ. Un échantillon relu et annoté à la main par l'équipe sert de jeu de test fiable, et les dix avis de data/sample_reviews.csv servent d'exemples dès le départ.

## Métrique de succès et seuil d'acceptation (obligatoire)

Le modèle est accepté si le rappel sur la classe négative est d'au moins 0,90 sur un jeu de test jamais vu, et si le F1 macro reste supérieur à 0,85. Autrement dit, sur 100 avis négatifs réels, au plus 10 peuvent passer sans alerte.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif manqué retarde la réponse à un client mécontent, alors qu'un avis positif classé négatif coûte seulement quelques secondes à un agent. Le modèle ne fait que trier : un agent relit toujours les avis prioritaires avant toute action, et un échantillon est revérifié régulièrement.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent contenir des noms, des numéros de commande ou des coordonnées : il faut les anonymiser avant l'entraînement et ne pas les conserver dans les journaux. Le modèle peut aussi se tromper sur l'ironie ou sur un vocabulaire absent de ses données, donc ses scores doivent être contrôlés sur des avis récents de ce site.

## Approche écartée et pourquoi (facultatif)

Les règles métier à base de mots-clés ont été écartées : elles ratent les formulations nuancées, l'ironie et les tournures nouvelles, et demandent une maintenance constante. Le modèle génératif seul a été écarté pour son coût par requête sur plusieurs milliers d'avis.