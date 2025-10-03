"""Vercel deployment entry point for Naramarket MCP Server."""

import os
import sys
import logging
from pathlib import Path

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel-mcp")

# Add the src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Set environment variables for Vercel deployment
os.environ.setdefault("FASTMCP_TRANSPORT", "http")
os.environ.setdefault("FASTMCP_HOST", "0.0.0.0")
os.environ.setdefault("PORT", "8000")

try:
    # Import FastMCP and create MCP instance
    from fastmcp import FastMCP
    from core.config import APP_NAME
    from tools.naramarket import naramarket_tools
    from tools.enhanced_tools import enhanced_tools
    
    logger.info("🚀 Initializing MCP for Vercel...")
    
    # Create FastMCP instance (same as main.py but without running)
    mcp = FastMCP(APP_NAME)
    
    # Register all tools (copy from main.py)
    @mcp.tool(name="server_info", description="Get server status and available tools list")
    def server_info():
        return naramarket_tools.server_info()
    
    @mcp.tool(name="get_recent_bid_announcements", description="최근 입찰공고 조회")
    def get_recent_bid_announcements(num_rows: int = 5, days_back: int = 7):
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        return enhanced_tools.call_public_data_standard_api(
            operation="getDataSetOpnStdBidPblancInfo",
            numOfRows=num_rows,
            pageNo=1,
            bidNtceBgnDt=start_date.strftime("%Y%m%d0000"),
            bidNtceEndDt=end_date.strftime("%Y%m%d2359")
        )
    
    @mcp.tool(name="search_shopping_mall_products", description="나라장터 쇼핑몰 제품 검색")
    def search_shopping_mall_products(product_name: str = None, company_name: str = None, num_rows: int = 5):
        kwargs = {}
        if product_name:
            kwargs["prdctClsfcNoNm"] = product_name
        if company_name:
            kwargs["cntrctCorpNm"] = company_name
        return enhanced_tools.call_shopping_mall_api(
            operation="getMASCntrctPrdctInfoList",
            numOfRows=num_rows,
            pageNo=1,
            **kwargs
        )
    
    # Create HTTP app for Vercel
    app = mcp.http_app()
    
    # Add welcome route for root path
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    
    async def welcome(request):
        return JSONResponse({
            "message": "🚀 Naramarket MCP Server (Vercel)",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "mcp": "/mcp",
                "api": "/api"
            }
        })
    
    # Add routes to existing app
    app.routes.insert(0, Route("/", welcome))
    
    logger.info("✅ MCP HTTP app created for Vercel")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize MCP: {e}")
    # Fallback simple app
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    
    async def health_check(request):
        return JSONResponse({
            "status": "error",
            "message": f"MCP initialization failed: {str(e)}",
            "server": "naramarket-mcp-vercel",
            "version": "2.0.0"
        }, status_code=500)
    
    async def fallback_handler(request):
        return JSONResponse({
            "error": "MCP Server not available",
            "message": str(e),
            "endpoints": {
                "health": "/health"
            }
        }, status_code=500)
    
    app = Starlette(routes=[
        Route("/health", health_check),
        Route("/", fallback_handler),
        Route("/{path:path}", fallback_handler)
    ])

# Export the ASGI app for Vercel
# Vercel will call this app for each request
