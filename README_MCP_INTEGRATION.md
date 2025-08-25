# MCP Integration Guide

This document explains how the MCP (Model Context Protocol) server integration works with the LangGraph agents.

## Architecture Overview

The integration bridges MCP tools with LangChain/LangGraph agents using `langchain-mcp-adapters`:

```
LangGraph Agent
     ↓
get_tools() [app/tools/__init__.py]
     ↓
get_mcp_tools() [app/tools/mcp_client.py]
     ↓
MCP Server [mcp_server/server.py]
     ↓
NASCAR Simulator API
```

## Key Components

### 1. MCP Server (`mcp_server/server.py`)
- Provides 24+ NASCAR-specific tools via FastMCP
- Supports dual transport modes: stdio (default) and HTTP
- Connects to the edge_server/web_server for real NASCAR data

### 2. MCP Client (`app/tools/mcp_client.py`)
- Uses `langchain-mcp-adapters` to discover MCP tools
- Converts MCP tools to LangChain BaseTool format
- Handles both stdio and HTTP transports
- Provides graceful fallback if MCP server is unavailable

### 3. Tool Registry (`app/tools/__init__.py`)
- Merges RAG knowledge tools with MCP server tools
- Agents automatically get all available tools via `get_tools()`
- No changes needed to existing agents

## Running the System

### Option 1: stdio Transport (Default - Development)
```bash
# The MCP server starts automatically when agents request tools
# No separate server process needed
python run_agent.py
```

### Option 2: HTTP Transport (Production)
```bash
# Terminal 1: Start MCP server in HTTP mode
python mcp_server/server.py --transport http --port 8000

# Terminal 2: Configure and run agent
export MCP_TRANSPORT=http
export MCP_PORT=8000
python run_agent.py
```

## Configuration

Environment variables for MCP integration:
- `MCP_TRANSPORT`: Transport type ('stdio' or 'http', default: 'stdio')
- `MCP_HOST`: Host for HTTP transport (default: '127.0.0.1')
- `MCP_PORT`: Port for HTTP transport (default: 8000)

## Benefits

1. **Zero Agent Changes**: Existing agents automatically get MCP tools
2. **Dynamic Discovery**: New MCP tools are immediately available
3. **Graceful Degradation**: System works even if MCP server is offline
4. **Production Ready**: Supports both development (stdio) and production (HTTP) modes
5. **Standard Protocol**: Uses the official Model Context Protocol

## Troubleshooting

If MCP tools aren't loading:

1. **Test MCP server directly**:
   ```bash
   python mcp_server/server.py
   ```

## How Agents Use MCP Tools

Agents don't need to know about MCP. They simply call `get_tools()` which now includes:
- Original RAG knowledge tools
- All MCP server tools (when available)

Example in `analytics_agent.py`:
```python
def analyze_query(state: PitBoxState) -> Dict[str, Any]:
    model = get_chat_model(model_name=ANALYTICS_MODEL)
    tools = get_tools()  # Now includes MCP tools!
    model_with_tools = model.bind_tools(tools)
    # ... rest of the code
```

The agent can now use tools like:
- `check_system_health_tool`
- `get_car_position_tool` 
- `analyze_pit_strategy_tool`
- And 20+ more NASCAR-specific tools