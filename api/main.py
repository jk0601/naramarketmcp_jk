"""Vercel Python serverless function - Fixed version."""

from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
import os

async def handle_root(request):
    """Root endpoint - return plain text to avoid download issues."""
    return PlainTextResponse(
        "🚀 Naramarket MCP Server is running on Vercel!\n\n"
        "Available endpoints:\n"
        "- GET /health (JSON)\n"
        "- GET /info (JSON)\n"
        "- GET /test (JSON)\n\n"
        "Server Status: ✅ Running\n"
        f"API Key: {'✅ Configured' if os.environ.get('NARAMARKET_SERVICE_KEY') else '❌ Missing'}"
    )

async def handle_health(request):
    """Health check endpoint."""
    return JSONResponse(
        {
            "status": "healthy",
            "server": "naramarket-mcp-vercel",
            "version": "2.0.3",
            "deployment": "vercel",
            "api_key_configured": bool(os.environ.get('NARAMARKET_SERVICE_KEY')),
            "endpoints": ["/", "/health", "/info", "/test"]
        },
        media_type="application/json"
    )

async def handle_info(request):
    """System information."""
    return JSONResponse(
        {
            "system_info": {
                "working_directory": os.getcwd(),
                "environment": {
                    "FASTMCP_TRANSPORT": os.environ.get('FASTMCP_TRANSPORT'),
                    "PORT": os.environ.get('PORT'),
                    "API_KEY_SET": bool(os.environ.get('NARAMARKET_SERVICE_KEY'))
                }
            },
            "server": "naramarket-vercel",
            "timestamp": "2024-10-03"
        },
        media_type="application/json"
    )

async def handle_test(request):
    """Simple test endpoint."""
    return JSONResponse(
        {
            "test": "success",
            "message": "All systems operational",
            "request_method": request.method,
            "request_path": request.url.path,
            "working": True
        },
        media_type="application/json"
    )

# Create Starlette application with explicit routes
app = Starlette(
    routes=[
        Route("/", handle_root, methods=["GET"]),
        Route("/health", handle_health, methods=["GET"]),
        Route("/info", handle_info, methods=["GET"]),
        Route("/test", handle_test, methods=["GET"]),
    ]
)

# Vercel will use this app as the ASGI application