# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Répondre automatiquement aux questions des étudiants sur le règlement intérieur de l'école (absences, examens, discipline, rattrapages), en s'appuyant sur le texte officiel.

## Utilisateur final (obligatoire)

L'étudiant, qui pose sa question en langage naturel, et indirectement l'administration (scolarité), qui reçoit moins de demandes répétitives.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Les documents du règlement existent déjà, mais l'école ne dispose pas de questions étiquetées, ce qui exclut le machine learning supervisé (a). La réponse doit être vérifiable : le RAG cite l'article exact dont elle provient, ce que l'étudiant peut contrôler (b). Une réponse inventée sur une règle peut pénaliser un étudiant (absence, examen), donc la réponse doit rester ancrée dans le texte officiel (d).

## Données nécessaires et leur origine (obligatoire)

Le règlement intérieur de l'école et les documents associés (charte des examens, règles d'absence), fournis par la scolarité dans leur version en vigueur. Une cinquantaine de questions de test, rédigées avec la scolarité, chacune associée à l'article de référence.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur les 50 questions de test, le bon article doit figurer parmi les 3 passages retrouvés dans au moins 90 % des cas, et au moins 90 % des réponses doivent être fidèles au texte et citer leur source. Pour une question hors règlement, le système doit répondre qu'il ne sait pas plutôt que d'inventer.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une mauvaise réponse peut conduire un étudiant à manquer une règle et à subir une sanction. Chaque réponse affiche donc l'article cité et précise que seul le texte officiel fait foi, et les cas ambigus ou sensibles sont renvoyés vers la scolarité.

## Risques éthiques ou de confidentialité (obligatoire)

Le règlement est un document public pour les étudiants, mais leurs questions peuvent contenir des informations personnelles (cas d'absence, situation disciplinaire) : il ne faut pas conserver les noms dans les journaux. Il faut aussi garder le règlement à jour, car une version périmée donnerait des réponses fausses.

## Approche écartée et pourquoi (facultatif)

Le modèle génératif seul a été écarté : il peut inventer des règles qui n'existent pas et ne permet pas de remonter à l'article d'origine, ce qui rend la réponse invérifiable.