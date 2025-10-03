"""Clean Vercel deployment entry point - NEW FILE."""

import os
import sys
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def root_handler(request):
    """Root endpoint."""
    return JSONResponse({
        "message": "🚀 Naramarket MCP Server (Clean Version)",
        "version": "2.0.1",
        "status": "running",
        "deployment": "vercel-clean",
        "timestamp": "2024-10-03-v2",
        "endpoints": {
            "health": "/health",
            "info": "/info"
        }
    })

async def health_handler(request):
    """Health check."""
    return JSONResponse({
        "status": "healthy",
        "server": "naramarket-vercel-clean",
        "version": "2.0.1",
        "environment": {
            "has_api_key": bool(os.environ.get('NARAMARKET_SERVICE_KEY')),
            "transport": os.environ.get('FASTMCP_TRANSPORT', 'default')
        }
    })

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

# Create clean Starlette app
app = Starlette(routes=[
    Route("/", root_handler, methods=["GET"]),
    Route("/health", health_handler, methods=["GET"]),
    Route("/info", info_handler, methods=["GET"]),
])
