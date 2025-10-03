"""Clean Vercel deployment entry point - NEW FILE."""

import os
import sys
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route

async def root_handler(request):
    """Root endpoint."""
    return JSONResponse(
        {
            "message": "🚀 Naramarket MCP Server (Clean Version)",
            "version": "2.0.1",
            "status": "running",
            "deployment": "vercel-clean",
            "timestamp": "2024-10-03-v2",
            "endpoints": {
                "health": "/health",
                "info": "/info"
            }
        },
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "no-cache"
        }
    )

async def health_handler(request):
    """Health check."""
    return JSONResponse(
        {
            "status": "healthy",
            "server": "naramarket-vercel-clean",
            "version": "2.0.1",
            "environment": {
                "has_api_key": bool(os.environ.get('NARAMARKET_SERVICE_KEY')),
                "transport": os.environ.get('FASTMCP_TRANSPORT', 'default')
            }
        },
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

async def info_handler(request):
    """System info."""
    return JSONResponse({
        "system": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
            "cwd": os.getcwd(),
            "env_vars": {
                "FASTMCP_TRANSPORT": os.environ.get('FASTMCP_TRANSPORT'),
                "PORT": os.environ.get('PORT'),
                "API_KEY_EXISTS": bool(os.environ.get('NARAMARKET_SERVICE_KEY'))
            }
        }
    })

async def html_test(request):
    """HTML test page."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Naramarket MCP Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .status { color: green; font-weight: bold; }
            .endpoint { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🚀 Naramarket MCP Server</h1>
        <p class="status">Status: Running on Vercel</p>
        <h2>Available Endpoints:</h2>
        <div class="endpoint"><strong>GET /</strong> - This page</div>
        <div class="endpoint"><strong>GET /health</strong> - Health check (JSON)</div>
        <div class="endpoint"><strong>GET /info</strong> - System info (JSON)</div>
        <div class="endpoint"><strong>GET /json</strong> - JSON test</div>
        
        <h2>Test JSON Response:</h2>
        <button onclick="testJson()">Test JSON Endpoint</button>
        <pre id="result"></pre>
        
        <script>
        async function testJson() {
            try {
                const response = await fetch('/json');
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').textContent = 'Error: ' + error.message;
            }
        }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

async def json_test(request):
    """Pure JSON test."""
    return JSONResponse(
        {
            "test": "success",
            "message": "JSON response working correctly",
            "timestamp": "2024-10-03",
            "browser_test": True
        },
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
        }
    )

# Create clean Starlette app
app = Starlette(routes=[
    Route("/", html_test, methods=["GET"]),
    Route("/health", health_handler, methods=["GET"]),
    Route("/info", info_handler, methods=["GET"]),
    Route("/json", json_test, methods=["GET"]),
    Route("/api", root_handler, methods=["GET"]),  # JSON endpoint
])
