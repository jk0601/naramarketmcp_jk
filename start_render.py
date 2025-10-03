#!/usr/bin/env python3
"""Render.com deployment entry point for Naramarket MCP Server."""

import os
import sys
import logging
from pathlib import Path

# Configure logging for Render
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("render-startup")

def main():
    """Main entry point for Render deployment."""
    logger.info("🚀 Starting Naramarket MCP Server on Render.com")
    
    # Set environment variables for Render
    os.environ.setdefault("FASTMCP_TRANSPORT", "http")
    os.environ.setdefault("FASTMCP_HOST", "0.0.0.0")
    
    # Get port from Render environment
    port = os.environ.get("PORT", "10000")
    os.environ["PORT"] = port
    
    logger.info(f"🌐 Server will start on port {port}")
    logger.info(f"🔑 API Key configured: {'✅' if os.environ.get('NARAMARKET_SERVICE_KEY') else '❌'}")
    
    # Import and run the main server
    try:
        # Add src to path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from main import main as server_main
        return server_main()
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
