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
            "health": "/api/health",
            "mcp": "/api/mcp",
            "api_test": "/api/"
        },
        "usage": "This is a Model Context Protocol (MCP) server for Korean government procurement data.",
        "documentation": "https://github.com/your-repo/naramarketmcp"
    })

async def health_check(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "server": "naramarket-mcp-vercel",
        "version": "2.0.0",
        "transport": "HTTP",
        "deployment": "vercel"
    })

# Create Starlette app for root routes
app = Starlette(routes=[
    Route("/", welcome),
    Route("/health", health_check),
])

# Export for Vercel
handler = app
