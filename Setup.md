
# NanoMind




## Lancement

Pour ouvrir ce projet, installez les fichiers, ouvrez le dans un ide avec un environement python prédéfinis, puis entrez cette commande :

```bash
  python train.py
```

Après avoir fait cette commande, un fucguer chatbot_model.h5 sera généré, c'est votre ia, ensuite, pour l'ouvrir il faut executer cette commande : 

```bash
  python load.py
```

Et le projet nanomind est setup !

Pour lui apprendre plus de phrases, vous pouvez ajouter des questions et des réponses dans intents.json, voici un exemple : 

```json
    "intents": [
        {
            "tag": "salutation",
            "patterns": [
                "Bonjour",
                "Salut"
            ],
            "responses": [
                "Bonjour",
                "Hey !"
            ]
        },
```

ici, quand on lui dicte un mot qui ressemble à bonjour ou salut, il répondras automatiquement un mot parmis ceux-dessous.

Quand il engage une conversation avec vous, il dis à quel point il est sur de sa réponse, exemple : 

```bash
Vous: Hey !
1/1 [==============================] - 0s 84ms/step
Bot : Salut ! Comment puis-je t'aider ? (0.9999001)
```

le nombre entre parenthèse se trouve entre 0 et 1.
N'hésitez pas à fork ce projet et y ajouter vos propres intents.json !