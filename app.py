"""Alternative deployment file for Render or other platforms."""

import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def root(request):
    return JSONResponse({
        "message": "🚀 Naramarket MCP Server (Alternative)",
        "version": "2.0.2",
        "status": "healthy",
        "platform": "render-ready",
        "endpoints": ["/health", "/test"]
    })

async def health(request):
    return JSONResponse({
        "status": "healthy",
        "server": "naramarket-alternative",
        "api_key_set": bool(os.environ.get('NARAMARKET_SERVICE_KEY'))
    })

async def test(request):
    return JSONResponse({
        "test": "success",
        "message": "Server is working perfectly!",
        "timestamp": "2024-10-03"
    })

app = Starlette(routes=[
    Route("/", root),
    Route("/health", health),
    Route("/test", test),
])

# For Render.com or other platforms
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
