Semaine 3 :


1. Pourquoi l'API refuse-t-elle de démarrer sans models/sentiment.joblib, plutôt que de démarrer et de répondre 503 ?

Quand j'ai retiré le modèle (Rename-Item models\sentiment.joblib sentiment.bak) puis lancé uvicorn api.main:app, le serveur ne démarre pas. La trace passe par lifespan (api/main.py, ligne 23), load_model(), SentimentClassifier.__init__, puis charger_modele(), qui lève FileNotFoundError: models/sentiment.joblib absent : lancez python src/train.py. Uvicorn termine avec Application startup failed. Exiting. et aucun serveur n'écoute.

C'est préférable à un démarrage suivi de réponses 503, pour trois raisons. L'erreur apparaît tout de suite, au lancement, avec un message qui dit quoi faire. Une API qui démarrerait sans modèle aurait l'air vivante (processus actif, /docs accessible) et la panne ne se découvrirait qu'à la première requête d'un client. Enfin, le modèle est chargé une seule fois, au démarrage : si ce chargement échoue, le service ne peut rien faire d'utile, autant s'arrêter. Le 503 de _classifier() reste utile comme filet de sécurité : il ne répond que si le classifieur manque dans app.state alors que le service tourne déjà, un cas que le TP4 teste.

2. Un texte vide est refusé deux fois : par Pydantic, puis par predict(). Est-ce redondant ?

Pas tout à fait. Mes essais donnent deux refus différents. {"text": ""} reçoit un 422 dont detail est une liste (type: string_too_short, loc: ["body", "text"], « String should have at least 1 character ») : c'est Pydantic, par min_length=1 dans api/schemas.py. {"text": "   "} (trois espaces) reçoit aussi un 422, mais detail est une simple chaîne, "texte vide" : le contrat l'a laissé passer, puisqu'il compte trois caractères, et c'est predict() qui l'a refusé (un ValueError, converti en 422 par main.py).

Les deux contrôles ne sont donc pas des doublons : le second attrape ce que le premier ne voit pas, et il est normal que predict() se protège, puisqu'on peut l'appeler sans passer par l'API. Mais le résultat est incohérent : un même défaut (texte vide ou blanc) produit deux formes de réponse, et un client doit gérer une liste ou une chaîne. La règle devrait être écrite une seule fois, dans le contrat, pour que l'API refuse les deux cas avec le même format, predict() restant une protection de dernier recours. D'après ma lecture de main.py (je ne l'ai pas observé), tout ValueError levé par le modèle devient aussi un 422, donc un bug interne pourrait être pris pour une faute du client.