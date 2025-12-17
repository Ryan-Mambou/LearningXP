"""
Example test file to demonstrate CI failure when bugs are introduced.
This file contains a test that will fail if a bug is introduced in the code.
"""

import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def reset_users():
    """Reset users list to initial state before each test."""
    from app import users
    users.clear()
    users.extend([
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ])
    yield
    users.clear()
    users.extend([
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ])

def test_home_endpoint_returns_correct_message(client):
    """
    This test will fail if the home endpoint message is changed incorrectly.
    This demonstrates how CI catches bugs.
    """
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    # This assertion will fail if someone accidentally changes the message
    assert data['message'] == "Welcome to the Flask API!"
    assert isinstance(data['message'], str)
    assert len(data['message']) > 0

def test_health_endpoint_always_returns_healthy(client):
    """
    This test ensures the health endpoint always returns 'healthy'.
    If someone breaks this, CI will fail.
    """
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == "healthy"

def test_user_creation_requires_both_fields(client, reset_users):
    """
    This test ensures that user creation requires both name and email.
    If validation is broken, this test will fail.
    """
    # Test missing name
    response = client.post(
        '/api/users',
        data=json.dumps({"email": "test@example.com"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    # Test missing email
    response = client.post(
        '/api/users',
        data=json.dumps({"name": "Test User"}),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_get_nonexistent_user_returns_404(client, reset_users):
    """
    This test ensures proper error handling for non-existent users.
    If error handling is broken, CI will catch it.
    """
    response = client.get('/api/users/99999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "User not found"

