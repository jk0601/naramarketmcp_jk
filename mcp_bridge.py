#!/usr/bin/env python3
"""
MCP HTTP Bridge for Claude Desktop
Vercel 배포된 MCP 서버를 Claude Desktop에서 사용하기 위한 브릿지
"""

import sys
import json
import requests
import asyncio
from typing import Dict, Any

# Vercel 배포 URL (배포 후 실제 URL로 변경하세요)
VERCEL_MCP_URL = "https://your-project.vercel.app/mcp"

class MCPHTTPBridge:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Claude-Desktop-MCP-Bridge/1.0'
        })
    
    def send_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send MCP request to HTTP server and return response."""
        try:
            response = self.session.post(
                self.server_url,
                json=message,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"HTTP request failed: {str(e)}"
                }
            }
        except json.JSONDecodeError as e:
            return {
                "jsonrpc": "2.0", 
                "id": message.get("id"),
                "error": {
                    "code": -32700,
                    "message": f"Invalid JSON response: {str(e)}"
                }
            }
    
    def run_stdio_bridge(self):
        """Run STDIO bridge for Claude Desktop."""
        try:
            # Read from stdin and write to stdout (Claude Desktop protocol)
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse JSON-RPC message from Claude Desktop
                    message = json.loads(line)
                    
                    # Forward to HTTP MCP server
                    response = self.send_request(message)
                    
                    # Send response back to Claude Desktop
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"Bridge error: {str(e)}\n")
            sys.exit(1)

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = VERCEL_MCP_URL
    
    bridge = MCPHTTPBridge(server_url)
    bridge.run_stdio_bridge()

if __name__ == "__main__":
    main()
