# Simple Flask API

A simple REST API built with Flask, with CI/CD pipeline for automated testing and deployment.

## Setup

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Running Tests

Run all tests:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

**Optionnel**: Vous pouvez aussi utiliser `./run_tests.sh` pour lancer les tests facilement (c'est juste un raccourci, pas nécessaire).

## CI/CD Pipeline

This project includes a GitHub Actions CI/CD pipeline that:

### Phase 1: Continuous Integration

- ✅ Runs unit and integration tests automatically on push/PR
- ✅ Tests against multiple Python versions (3.9, 3.10, 3.11)
- ✅ Performs code quality checks with flake8
- ✅ Generates test coverage reports
- ✅ **Fails if bugs are introduced** - see `BUG_EXAMPLE.md` for details

### Phase 2: Continuous Deployment

- ✅ Automatically deploys to **Azure VM** after merge to `main`/`master`
- ✅ Only deploys if all tests pass
- ✅ **Uses Terraform for Infrastructure as Code deployment on Azure**
- ✅ Creates and manages Azure resources (VM, network, security groups)
- ✅ Uses SSH for secure deployment
- ✅ Manages application as a systemd service
- ✅ Zero-downtime deployment with automatic restart
- ✅ Idempotent deployments (only redeploys when files change)

### How it works

1. **On Push/PR**: Tests and linting run automatically
2. **On Merge to Main**: If tests pass, Terraform deployment job triggers
3. **Deployment Process** (via Terraform on Azure):
   - Authenticates with Azure using Service Principal
   - Terraform creates/manages Azure resources (Resource Group, VNet, VM, etc.)
   - Connects to Azure VM via SSH
   - Copies application files (app.py, requirements.txt)
   - Installs Python dependencies
   - Creates systemd service
   - Starts the application automatically
   - Only redeploys if files have changed (idempotent)

### Testing CI Failure

To verify that the CI correctly fails when bugs are introduced:

- See `BUG_EXAMPLE.md` for examples of bugs that will cause CI to fail
- Introduce a bug, commit, and push - the CI should fail

### Deployment Setup (Azure)

**📖 Guide Simple:** Voir `SETUP_SIMPLE.md` pour un guide étape par étape.

**Pour déploiement automatique (GitHub Actions):**

1. Un seul secret nécessaire: `AZURE_CREDENTIALS`
2. Créez-le avec: `az ad sp create-for-rbac --name "github-actions-learningxp" --role="Contributor" --scopes="/subscriptions/YOUR_SUB_ID" --sdk-auth`
3. Ajoutez le JSON comme secret dans GitHub
4. Mergez sur `main` → Déploiement automatique ! ✨

**Pour déploiement local:**

1. `cd terraform`
2. `cp terraform.tfvars.example terraform.tfvars`
3. Ajoutez votre clé SSH publique dans `terraform.tfvars`
4. `terraform init && terraform apply`

## Endpoints

- `GET /` - Welcome message
- `GET /api/health` - Health check endpoint
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get a specific user by ID
- `POST /api/users` - Create a new user (requires JSON body with `name` and `email`)

## Example Usage

### Get all users

```bash
curl http://localhost:5000/api/users
```

### Get a specific user

```bash
curl http://localhost:5000/api/users/1
```

### Create a new user

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

# LearningXP

subscriptionId: 6a4a8382-7921-4a45-8464-6f38c8dda2ee
