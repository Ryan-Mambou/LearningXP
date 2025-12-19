#!/usr/bin/env python3
"""
Simple HTTP server for the LearningXP web application.
Serves static files and provides a REST API.
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import mimetypes

# Sample data
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

class WebAppHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for the web application."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API endpoints
        if path == '/api/users':
            self.handle_get_users()
        elif path.startswith('/api/users/'):
            user_id = path.split('/')[-1]
            self.handle_get_user(user_id)
        elif path == '/api/health':
            self.handle_health()
        # Serve static files
        elif path.startswith('/static/'):
            self.handle_static_file(path)
        # Serve index.html for root
        elif path == '/' or path == '/index.html':
            self.handle_static_file('/index.html')
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/users':
            self.handle_create_user()
        else:
            self.send_error(404, "Not Found")
    
    def handle_get_users(self):
        """Handle GET /api/users - Get all users."""
        self.send_json_response(200, {"users": users})
    
    def handle_get_user(self, user_id):
        """Handle GET /api/users/<id> - Get user by ID."""
        try:
            user_id = int(user_id)
            user = next((u for u in users if u["id"] == user_id), None)
            if user:
                self.send_json_response(200, user)
            else:
                self.send_json_response(404, {"error": "User not found"})
        except ValueError:
            self.send_json_response(404, {"error": "Invalid user ID"})
    
    def handle_create_user(self):
        """Handle POST /api/users - Create a new user."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if not data.get('name') or not data.get('email'):
                self.send_json_response(400, {"error": "Name and email are required"})
                return
            
            new_user = {
                "id": len(users) + 1,
                "name": data["name"],
                "email": data["email"]
            }
            users.append(new_user)
            self.send_json_response(201, new_user)
        except json.JSONDecodeError:
            self.send_json_response(400, {"error": "Invalid JSON"})
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def handle_health(self):
        """Handle GET /api/health - Health check endpoint."""
        self.send_json_response(200, {"status": "healthy"})
    
    def handle_static_file(self, path):
        """Serve static files."""
        # Remove leading slash
        file_path = path.lstrip('/')
        
        # Security: prevent directory traversal
        if '..' in file_path:
            self.send_error(403, "Forbidden")
            return
        
        # Default to index.html if path is empty
        if not file_path or file_path == '/':
            file_path = 'index.html'
        
        # Check if file exists
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = 'application/octet-stream'
        
        # Read and send file
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")
    
    def send_json_response(self, status_code, data):
        """Send JSON response."""
        json_data = json.dumps(data, indent=2)
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize log format."""
        # Suppress default logging or customize it
        pass

def run_server(port=5000):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebAppHandler)
    print(f"Server running on http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    run_server(port)

