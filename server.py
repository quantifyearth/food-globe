#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/api/countries':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Get list of available countries from directory structure
            countries = []
            for item in os.listdir('.'):
                if os.path.isdir(item) and len(item) == 3 and item.islower():
                    impact_file = os.path.join(item, 'impact_paths.json')
                    if os.path.exists(impact_file):
                        countries.append(item)
            
            self.wfile.write(json.dumps(sorted(countries)).encode())
            return
        
        # Default handler for other requests
        super().do_GET()

if __name__ == "__main__":
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Open http://localhost:8000 in your browser")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")