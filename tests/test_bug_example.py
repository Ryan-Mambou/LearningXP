"""
Example test file to demonstrate CI failure when bugs are introduced.
This file contains a test that will fail if a bug is introduced in the code.
"""

import pytest
import json
import http.client
from server import users, WebAppHandler
from http.server import HTTPServer
import threading
import time

# Test server setup
TEST_PORT = 8889
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

def test_home_endpoint_returns_html(test_server):
    """
    This test ensures the home endpoint returns HTML.
    If someone breaks this, CI will fail.
    """
    conn = http.client.HTTPConnection('localhost', TEST_PORT)
    try:
        conn.request('GET', '/')
        response = conn.getresponse()
        assert response.status == 200
        assert 'text/html' in response.getheader('Content-Type', '')
        html_content = response.read().decode('utf-8')
        assert 'LearningXP' in html_content
    finally:
        conn.close()

def test_health_endpoint_always_returns_healthy(test_server):
    """
    This test ensures the health endpoint always returns 'healthy'.
    If someone breaks this, CI will fail.
    """
    status, data = make_request('GET', '/api/health')
    assert status == 200
    assert data['status'] == "healthy"

def test_user_creation_requires_both_fields(test_server, reset_users):
    """
    This test ensures that user creation requires both name and email.
    If validation is broken, this test will fail.
    """
    # Test missing name
    status, data = make_request('POST', '/api/users', json.dumps({"email": "test@example.com"}))
    assert status == 400
    assert 'error' in data
    
    # Test missing email
    status, data = make_request('POST', '/api/users', json.dumps({"name": "Test User"}))
    assert status == 400
    assert 'error' in data

def test_get_nonexistent_user_returns_404(test_server, reset_users):
    """
    This test ensures proper error handling for non-existent users.
    If error handling is broken, CI will catch it.
    """
    status, data = make_request('GET', '/api/users/99999')
    assert status == 404
    assert 'error' in data
    assert data['error'] == "User not found"
