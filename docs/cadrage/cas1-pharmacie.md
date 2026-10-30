# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter automatiquement les ordonnances dont il manque un champ obligatoire (patient, date, prescripteur, médicament, posologie, signature) avant qu'elles ne soient validées.

## Utilisateur final (obligatoire)

Le pharmacien et le préparateur au comptoir, qui saisissent ou scannent l'ordonnance avant la délivrance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

La liste des champs obligatoires est connue et stable, donc aucune donnée étiquetée n'est nécessaire pour l'apprendre (a). Chaque alerte est entièrement vérifiable, puisqu'elle nomme le champ précis qui manque (b). Une ordonnance validée à tort peut mettre le patient en danger, ce qui impose un comportement déterministe et auditable plutôt qu'un modèle probabiliste (d).

## Données nécessaires et leur origine (obligatoire)

La liste réglementaire des champs obligatoires, fournie par le pharmacien responsable. Une trentaine d'ordonnances anonymisées, complètes et incomplètes, servent à tester les règles.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un échantillon de 100 ordonnances annotées par un pharmacien, toutes les ordonnances incomplètes doivent être signalées (rappel de 100 %). Le taux de fausses alertes doit rester inférieur à 5 %.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une ordonnance incomplète non détectée peut conduire à une délivrance dangereuse, alors qu'une fausse alerte ne coûte que quelques secondes de vérification. Le pharmacien garde toujours la validation finale : l'outil signale, il ne décide pas.

## Risques éthiques ou de confidentialité (obligatoire)

Les ordonnances sont des données de santé : stockage chiffré, accès restreint, et jeux de test anonymisés. Le traitement doit respecter la loi 09-08 sur la protection des données personnelles (CNDP au Maroc).

## Approche écartée et pourquoi (facultatif)

Le machine learning a été écarté : il exigerait de nombreuses ordonnances étiquetées et ne garantirait pas un rappel de 100 % sur des champs dont la liste est déjà connue.