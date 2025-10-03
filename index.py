"""Root endpoint for Vercel deployment."""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def welcome(request):
    """Welcome page for root path."""
    return JSONResponse({
        "message": "🚀 Naramarket MCP Server is running on Vercel!",
        "version": "2.0.0",
        "status": "healthy",
        "endpoints": {
            "health": "/health",
            "mcp_server": "/api/",
            "api_docs": "Use POST /api/ for MCP calls"
        },
        "usage": "This is a Model Context Protocol (MCP) server for Korean government procurement data.",
        "github": "https://github.com/your-repo/naramarketmcp"
    })

async def health_check(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "server": "naramarket-mcp-vercel",
        "version": "2.0.0",
        "transport": "HTTP",
        "deployment": "vercel",
        "timestamp": "2024-10-03"
    })

# Create Starlette app for root routes
app = Starlette(routes=[
    Route("/", welcome, methods=["GET"]),
    Route("/health", health_check, methods=["GET"]),
])

# This is the ASGI application that Vercel will call
# No need for handler = app, just export app directly
