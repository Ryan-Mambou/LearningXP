# Exemple de Bug pour Tester la CI

Ce document explique comment tester que la CI/CD échoue correctement lorsqu'un bug est introduit dans le code.

## Comment tester

### Méthode 1 : Introduire un bug intentionnel

1. Modifiez `app.py` pour introduire un bug, par exemple :

```python
@app.route('/', methods=['GET'])
def home():
    # BUG: Changement du message qui cassera les tests
    return jsonify({"message": "Wrong message!"})
```

2. Commitez et poussez les changements :

```bash
git add app.py
git commit -m "Test: Introduce bug to verify CI fails"
git push
```

3. La CI devrait échouer car le test `test_home_endpoint_returns_correct_message` échouera.

### Méthode 2 : Casser une validation

1. Modifiez `app.py` pour retirer la validation :

```python
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # BUG: Retirer la validation
    # if not data or not data.get('name') or not data.get('email'):
    #     return jsonify({"error": "Name and email are required"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data.get("name", ""),  # Peut être vide maintenant
        "email": data.get("email", "")
    }
    users.append(new_user)
    return jsonify(new_user), 201
```

2. Les tests `test_user_creation_requires_both_fields` échoueront.

### Méthode 3 : Casser le code (erreur de syntaxe)

1. Introduisez une erreur de syntaxe dans `app.py` :

```python
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"  # BUG: Parenthèse manquante
```

2. La CI échouera lors de l'installation ou de l'exécution des tests.

## Vérification locale

Avant de pousser, vous pouvez tester localement :

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
pytest tests/ -v

# Si les tests passent, introduire un bug et relancer les tests
# Les tests devraient échouer
```

## Résultat attendu

Quand un bug est introduit et poussé sur la branche :

- ✅ La CI détecte le problème
- ✅ Le pipeline échoue avec un message d'erreur clair
- ✅ Le développeur est notifié de l'échec
- ✅ Le code défectueux n'est pas déployé
