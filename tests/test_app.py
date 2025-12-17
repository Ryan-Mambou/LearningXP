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

class TestHomeEndpoint:
    """Tests for the home endpoint."""
    
    def test_home_endpoint(self, client):
        """Test that home endpoint returns welcome message."""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Welcome to the Flask API!"

class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == "healthy"

class TestGetUsers:
    """Tests for GET /api/users endpoint."""
    
    def test_get_all_users(self, client, reset_users):
        """Test retrieving all users."""
        response = client.get('/api/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data
        assert len(data['users']) == 2
        assert data['users'][0]['name'] == "John Doe"
        assert data['users'][1]['name'] == "Jane Smith"
    
    def test_get_users_response_format(self, client, reset_users):
        """Test that users response has correct format."""
        response = client.get('/api/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data['users'], list)
        assert all('id' in user for user in data['users'])
        assert all('name' in user for user in data['users'])
        assert all('email' in user for user in data['users'])

class TestGetUser:
    """Tests for GET /api/users/<id> endpoint."""
    
    def test_get_existing_user(self, client, reset_users):
        """Test retrieving an existing user by ID."""
        response = client.get('/api/users/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['name'] == "John Doe"
        assert data['email'] == "john@example.com"
    
    def test_get_nonexistent_user(self, client, reset_users):
        """Test retrieving a non-existent user returns 404."""
        response = client.get('/api/users/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == "User not found"
    
    def test_get_user_invalid_id(self, client, reset_users):
        """Test retrieving user with invalid ID format."""
        response = client.get('/api/users/invalid')
        assert response.status_code == 404

class TestCreateUser:
    """Tests for POST /api/users endpoint."""
    
    def test_create_user_success(self, client, reset_users):
        """Test creating a new user successfully."""
        new_user = {
            "name": "Alice Johnson",
            "email": "alice@example.com"
        }
        response = client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == "Alice Johnson"
        assert data['email'] == "alice@example.com"
        assert data['id'] == 3
    
    def test_create_user_missing_name(self, client, reset_users):
        """Test creating user without name returns 400."""
        new_user = {
            "email": "test@example.com"
        }
        response = client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert "required" in data['error'].lower()
    
    def test_create_user_missing_email(self, client, reset_users):
        """Test creating user without email returns 400."""
        new_user = {
            "name": "Test User"
        }
        response = client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_user_empty_data(self, client, reset_users):
        """Test creating user with empty data returns 400."""
        response = client.post(
            '/api/users',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_create_user_no_json(self, client, reset_users):
        """Test creating user without JSON data returns 400."""
        response = client.post('/api/users')
        assert response.status_code == 400
    
    def test_create_user_increments_id(self, client, reset_users):
        """Test that creating users increments ID correctly."""
        # Create first user
        user1 = {"name": "User 1", "email": "user1@example.com"}
        response1 = client.post(
            '/api/users',
            data=json.dumps(user1),
            content_type='application/json'
        )
        assert response1.status_code == 201
        data1 = json.loads(response1.data)
        assert data1['id'] == 3
        
        # Create second user
        user2 = {"name": "User 2", "email": "user2@example.com"}
        response2 = client.post(
            '/api/users',
            data=json.dumps(user2),
            content_type='application/json'
        )
        assert response2.status_code == 201
        data2 = json.loads(response2.data)
        assert data2['id'] == 4

class TestIntegration:
    """Integration tests for multiple endpoints."""
    
    def test_create_and_retrieve_user(self, client, reset_users):
        """Test creating a user and then retrieving it."""
        # Create user
        new_user = {
            "name": "Bob Smith",
            "email": "bob@example.com"
        }
        create_response = client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        created_data = json.loads(create_response.data)
        user_id = created_data['id']
        
        # Retrieve user
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 200
        retrieved_data = json.loads(get_response.data)
        assert retrieved_data['name'] == "Bob Smith"
        assert retrieved_data['email'] == "bob@example.com"
    
    def test_user_appears_in_list_after_creation(self, client, reset_users):
        """Test that created user appears in users list."""
        # Get initial count
        initial_response = client.get('/api/users')
        initial_data = json.loads(initial_response.data)
        initial_count = len(initial_data['users'])
        
        # Create user
        new_user = {
            "name": "Charlie Brown",
            "email": "charlie@example.com"
        }
        client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        
        # Verify user appears in list
        final_response = client.get('/api/users')
        final_data = json.loads(final_response.data)
        assert len(final_data['users']) == initial_count + 1
        assert any(user['email'] == "charlie@example.com" for user in final_data['users'])

