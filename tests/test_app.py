import pytest
import json
import http.client
import urllib.parse
from server import WebAppHandler, users
from http.server import HTTPServer
import threading
import time

# Test server setup
TEST_PORT = 8888
BASE_URL = f"http://localhost:{TEST_PORT}"

@pytest.fixture(scope="module")
def test_server():
    """Start test server in a separate thread."""
    server = HTTPServer(('localhost', TEST_PORT), WebAppHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(0.5)
    
    yield server
    
    server.shutdown()
    server.server_close()

@pytest.fixture(autouse=True)
def reset_users():
    """Reset users list to initial state before each test."""
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

def make_request(method, path, body=None, headers=None):
    """Make HTTP request to test server."""
    conn = http.client.HTTPConnection('localhost', TEST_PORT)
    request_headers = {'Content-Type': 'application/json'} if body else {}
    if headers:
        request_headers.update(headers)
    
    try:
        conn.request(method, path, body, request_headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        return response.status, json.loads(data) if data else {}
    finally:
        conn.close()

class TestHomeEndpoint:
    """Tests for the home endpoint."""
    
    def test_home_endpoint(self, test_server):
        """Test that home endpoint returns HTML."""
        conn = http.client.HTTPConnection('localhost', TEST_PORT)
        try:
            conn.request('GET', '/')
            response = conn.getresponse()
            assert response.status == 200
            assert 'text/html' in response.getheader('Content-Type', '')
        finally:
            conn.close()

class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check(self, test_server, reset_users):
        """Test that health endpoint returns healthy status."""
        status, data = make_request('GET', '/api/health')
        assert status == 200
        assert data['status'] == "healthy"

class TestGetUsers:
    """Tests for GET /api/users endpoint."""
    
    def test_get_all_users(self, test_server, reset_users):
        """Test retrieving all users."""
        status, data = make_request('GET', '/api/users')
        assert status == 200
        assert 'users' in data
        assert len(data['users']) == 2
        assert data['users'][0]['name'] == "John Doe"
        assert data['users'][1]['name'] == "Jane Smith"
    
    def test_get_users_response_format(self, test_server, reset_users):
        """Test that users response has correct format."""
        status, data = make_request('GET', '/api/users')
        assert status == 200
        assert isinstance(data['users'], list)
        assert all('id' in user for user in data['users'])
        assert all('name' in user for user in data['users'])
        assert all('email' in user for user in data['users'])

class TestGetUser:
    """Tests for GET /api/users/<id> endpoint."""
    
    def test_get_existing_user(self, test_server, reset_users):
        """Test retrieving an existing user by ID."""
        status, data = make_request('GET', '/api/users/1')
        assert status == 200
        assert data['id'] == 1
        assert data['name'] == "John Doe"
        assert data['email'] == "john@example.com"
    
    def test_get_nonexistent_user(self, test_server, reset_users):
        """Test retrieving a non-existent user returns 404."""
        status, data = make_request('GET', '/api/users/999')
        assert status == 404
        assert 'error' in data
        assert data['error'] == "User not found"
    
    def test_get_user_invalid_id(self, test_server, reset_users):
        """Test retrieving user with invalid ID format."""
        status, data = make_request('GET', '/api/users/invalid')
        assert status == 404

class TestCreateUser:
    """Tests for POST /api/users endpoint."""
    
    def test_create_user_success(self, test_server, reset_users):
        """Test creating a new user successfully."""
        new_user = {
            "name": "Alice Johnson",
            "email": "alice@example.com"
        }
        status, data = make_request('POST', '/api/users', json.dumps(new_user))
        assert status == 201
        assert data['name'] == "Alice Johnson"
        assert data['email'] == "alice@example.com"
        assert data['id'] == 3
    
    def test_create_user_missing_name(self, test_server, reset_users):
        """Test creating user without name returns 400."""
        new_user = {
            "email": "test@example.com"
        }
        status, data = make_request('POST', '/api/users', json.dumps(new_user))
        assert status == 400
        assert 'error' in data
        assert "required" in data['error'].lower()
    
    def test_create_user_missing_email(self, test_server, reset_users):
        """Test creating user without email returns 400."""
        new_user = {
            "name": "Test User"
        }
        status, data = make_request('POST', '/api/users', json.dumps(new_user))
        assert status == 400
        assert 'error' in data
    
    def test_create_user_empty_data(self, test_server, reset_users):
        """Test creating user with empty data returns 400."""
        status, data = make_request('POST', '/api/users', json.dumps({}))
        assert status == 400
    
    def test_create_user_no_json(self, test_server, reset_users):
        """Test creating user without JSON data returns error."""
        conn = http.client.HTTPConnection('localhost', TEST_PORT)
        try:
            conn.request('POST', '/api/users', '', {'Content-Type': 'application/json'})
            response = conn.getresponse()
            assert response.status in [400, 500]
        finally:
            conn.close()
    
    def test_create_user_increments_id(self, test_server, reset_users):
        """Test that creating users increments ID correctly."""
        # Create first user
        user1 = {"name": "User 1", "email": "user1@example.com"}
        status1, data1 = make_request('POST', '/api/users', json.dumps(user1))
        assert status1 == 201
        assert data1['id'] == 3
        
        # Create second user
        user2 = {"name": "User 2", "email": "user2@example.com"}
        status2, data2 = make_request('POST', '/api/users', json.dumps(user2))
        assert status2 == 201
        assert data2['id'] == 4

class TestIntegration:
    """Integration tests for multiple endpoints."""
    
    def test_create_and_retrieve_user(self, test_server, reset_users):
        """Test creating a user and then retrieving it."""
        # Create user
        new_user = {
            "name": "Bob Smith",
            "email": "bob@example.com"
        }
        create_status, created_data = make_request('POST', '/api/users', json.dumps(new_user))
        assert create_status == 201
        user_id = created_data['id']
        
        # Retrieve user
        get_status, retrieved_data = make_request('GET', f'/api/users/{user_id}')
        assert get_status == 200
        assert retrieved_data['name'] == "Bob Smith"
        assert retrieved_data['email'] == "bob@example.com"
    
    def test_user_appears_in_list_after_creation(self, test_server, reset_users):
        """Test that created user appears in users list."""
        # Get initial count
        initial_status, initial_data = make_request('GET', '/api/users')
        initial_count = len(initial_data['users'])
        
        # Create user
        new_user = {
            "name": "Charlie Brown",
            "email": "charlie@example.com"
        }
        make_request('POST', '/api/users', json.dumps(new_user))
        
        # Verify user appears in list
        final_status, final_data = make_request('GET', '/api/users')
        assert len(final_data['users']) == initial_count + 1
        assert any(user['email'] == "charlie@example.com" for user in final_data['users'])
