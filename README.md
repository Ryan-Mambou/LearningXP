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

## CI/CD Pipeline

This project includes a GitHub Actions CI/CD pipeline that:

- ✅ Runs unit and integration tests automatically on push/PR
- ✅ Tests against multiple Python versions (3.9, 3.10, 3.11)
- ✅ Performs code quality checks with flake8
- ✅ Generates test coverage reports
- ✅ **Fails if bugs are introduced** - see `BUG_EXAMPLE.md` for details

### How it works

1. When you push code to `main`, `master`, or `develop` branches, the CI pipeline runs automatically
2. Tests are executed across multiple Python versions
3. Code quality checks are performed
4. If any test fails, the pipeline fails and prevents deployment

### Testing CI Failure

To verify that the CI correctly fails when bugs are introduced:
- See `BUG_EXAMPLE.md` for examples of bugs that will cause CI to fail
- Introduce a bug, commit, and push - the CI should fail

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
