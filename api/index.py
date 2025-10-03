"""Simple Vercel deployment entry point for debugging."""

import os
import sys
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def welcome(request):
    """Welcome page for root path."""
    return JSONResponse({
        "message": "🚀 Naramarket MCP Server (Debug Version)",
        "version": "2.0.0-debug",
        "status": "healthy",
        "deployment": "vercel",
        "endpoints": {
            "health": "/health",
            "debug": "/debug",
            "test": "/test"
        }
    })

async def health_check(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "server": "naramarket-mcp-vercel-debug",
        "version": "2.0.0",
        "transport": "HTTP",
        "deployment": "vercel",
        "environment": {
            "api_key_configured": bool(os.environ.get('NARAMARKET_SERVICE_KEY')),
            "transport_mode": os.environ.get('FASTMCP_TRANSPORT', 'not_set'),
            "port": os.environ.get('PORT', 'not_set')
        }
    })

async def debug_info(request):
    """Debug information."""
    try:
        files_list = os.listdir('.')
    except Exception as ex:
        files_list = [f"Error listing files: {str(ex)}"]
    
    return JSONResponse({
        "debug_info": {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "environment_variables": {
                "FASTMCP_TRANSPORT": os.environ.get('FASTMCP_TRANSPORT'),
                "FASTMCP_HOST": os.environ.get('FASTMCP_HOST'),
                "PORT": os.environ.get('PORT'),
                "API_KEY_SET": "Yes" if os.environ.get('NARAMARKET_SERVICE_KEY') else "No"
            },
            "files_in_root": files_list[:10],
            "python_path": sys.path[:3]
        }
    })

async def test_endpoint(request):
    """Test endpoint to verify basic functionality."""
    return JSONResponse({
        "test": "success",
        "message": "Basic Starlette app is working!",
        "request_method": request.method,
        "request_url": str(request.url)
    })

# Create Starlette application
app = Starlette(
    routes=[
        Route("/", welcome, methods=["GET"]),
        Route("/health", health_check, methods=["GET"]),
        Route("/debug", debug_info, methods=["GET"]),
        Route("/test", test_endpoint, methods=["GET"]),
    ]
)

# This is the ASGI app that Vercel will use