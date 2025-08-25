"""Tool registry"""

import logging
from typing import List

from langchain_core.tools import BaseTool

from .mcp_client import get_mcp_tools
from .rag_knowledge import get_knowledge_tools

logger = logging.getLogger(__name__)


def get_tools() -> List[BaseTool]:
    """Get all available tools"""
    tools = []

    # Get RAG knowledge tools
    tools.extend(get_knowledge_tools())

    # Get MCP server tools (NASCAR simulator tools)
    try:
        mcp_tools = get_mcp_tools()
        if mcp_tools:
            tools.extend(mcp_tools)
            logger.info(f"Loaded {len(mcp_tools)} tools from MCP server")
        else:
            logger.warning("No tools loaded from MCP server - server may be offline")
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")

    return tools
