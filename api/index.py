"""Vercel Python serverless function - Standard handler format."""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        
        # Route handling
        if path == '/' or path == '':
            self.handle_root()
        elif path == '/health':
            self.handle_health()
        elif path == '/info':
            self.handle_info()
        elif path == '/test':
            self.handle_test()
        else:
            self.handle_404()
    
    def handle_root(self):
        """Root endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        response = """🚀 Naramarket MCP Server (Vercel Standard Handler)

✅ Server Status: Running
✅ API Key: {}
✅ Version: 2.0.4

Available Endpoints:
- GET /health (JSON health check)
- GET /info (JSON system info)  
- GET /test (JSON test response)

This is working with Vercel's standard Python handler format.
""".format("Configured" if os.environ.get('NARAMARKET_SERVICE_KEY') else "Missing")
        
        self.wfile.write(response.encode('utf-8'))
    
    def handle_health(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        
        health_data = {
            "status": "healthy",
            "server": "naramarket-mcp-vercel-standard",
            "version": "2.0.4",
            "deployment": "vercel-python-handler",
            "api_key_configured": bool(os.environ.get('NARAMARKET_SERVICE_KEY')),
            "transport": os.environ.get('FASTMCP_TRANSPORT', 'http'),
            "endpoints": ["/", "/health", "/info", "/test"]
        }
        
        self.wfile.write(json.dumps(health_data, indent=2).encode('utf-8'))
    
    def handle_info(self):
        """System info endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        
        info_data = {
            "system": {
                "working_directory": os.getcwd(),
                "python_version": "3.12",
                "platform": "vercel-serverless"
            },
            "environment": {
                "FASTMCP_TRANSPORT": os.environ.get('FASTMCP_TRANSPORT'),
                "PORT": os.environ.get('PORT'),
                "API_KEY_SET": bool(os.environ.get('NARAMARKET_SERVICE_KEY'))
            },
            "server": "naramarket-vercel-standard",
            "timestamp": "2024-10-03",
            "handler_type": "BaseHTTPRequestHandler"
        }
        
        self.wfile.write(json.dumps(info_data, indent=2).encode('utf-8'))
    
    def handle_test(self):
        """Test endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        
        test_data = {
            "test": "success",
            "message": "Vercel Python handler working correctly!",
            "path": self.path,
            "method": self.command,
            "working": True,
            "timestamp": "2024-10-03"
        }
        
        self.wfile.write(json.dumps(test_data, indent=2).encode('utf-8'))
    
    def handle_404(self):
        """404 handler."""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        
        error_data = {
            "error": "Not Found",
            "message": f"Path '{self.path}' not found",
            "available_paths": ["/", "/health", "/info", "/test"],
            "status": 404
        }
        
        self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
