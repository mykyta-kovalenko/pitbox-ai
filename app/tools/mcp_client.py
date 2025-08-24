"""MCP Client integration for discovering and using MCP server tools."""

import asyncio
import logging
import os
from pathlib import Path
from typing import List, Optional

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger(__name__)


class MCPToolsClient:
    """Client for discovering and using MCP server tools."""

    def __init__(
        self,
        transport: str = "stdio",
        server_path: Optional[str] = None,
        host: str = "127.0.0.1",
        port: int = 8000,
    ):
        """Initialize MCP client.

        Args:
            transport: Transport type - 'stdio' or 'http'
            server_path: Path to MCP server script (for stdio)
            host: Host for HTTP transport
            port: Port for HTTP transport
        """
        self.transport = transport
        self.server_path = server_path or str(
            Path(__file__).parent.parent.parent / "mcp_server" / "server.py"
        )
        self.host = host
        self.port = port
        self._client = None
        self._tools = []

    async def _initialize_client(self) -> MultiServerMCPClient:
        """Initialize the MCP client based on transport type."""
        if self.transport == "stdio":
            # Configure for stdio transport
            config = {
                "trackhouse": {
                    "command": "python",
                    "args": [self.server_path],
                    "transport": "stdio",
                }
            }
        else:  # http
            # Configure for HTTP transport
            config = {
                "trackhouse": {
                    "url": f"http://{self.host}:{self.port}",
                    "transport": "sse",  # MCP adapters use SSE for HTTP
                }
            }

        return MultiServerMCPClient(config)

    async def get_tools_async(self) -> List[BaseTool]:
        """Get tools from MCP server asynchronously."""
        try:
            if not self._client:
                self._client = await self._initialize_client()

            # Get tools from the MCP server
            self._tools = await self._client.get_tools()
            logger.info(f"Successfully loaded {len(self._tools)} tools from MCP server")
            return self._tools

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            # Return empty list if connection fails - graceful degradation
            return []

    def get_tools(self) -> List[BaseTool]:
        """Get tools from MCP server (synchronous wrapper)."""
        # Check if we're in an async context
        try:
            asyncio.get_running_loop()
            # We're in an async context, create a new thread
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.get_tools_async())
                return future.result()
        except RuntimeError:
            # No async loop, we can run directly
            return asyncio.run(self.get_tools_async())


def get_mcp_tools(
    transport: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> List[BaseTool]:
    """Convenience function to get MCP tools.

    Args:
        transport: Override transport from environment
        host: Override host from environment
        port: Override port from environment

    Returns:
        List of MCP tools as LangChain tools
    """
    # Get configuration from environment or use defaults
    transport = transport or os.getenv("MCP_TRANSPORT", "stdio")
    host = host or os.getenv("MCP_HOST", "127.0.0.1")
    port = port or int(os.getenv("MCP_PORT", "8000"))

    client = MCPToolsClient(transport=transport, host=host, port=port)
    return client.get_tools()
