"""Tool registry"""

from typing import List

from langchain_core.tools import BaseTool

from .rag_knowledge import get_knowledge_tools

# from .simulator_api import get_simulator_tools


def get_tools() -> List[BaseTool]:
    """Get all available tools."""
    tools = []
    tools.extend(get_knowledge_tools())
    # Add simulator tools when implemented
    # tools.extend(get_simulator_tools())
    return tools
