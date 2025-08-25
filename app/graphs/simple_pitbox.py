"""Simple NASCAR Pit Box Agent - Basic Q&A with tool routing"""

import asyncio
from functools import lru_cache
from typing import Any, Dict, Literal

from langchain_core.messages import ToolMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from ..models import get_chat_model
from ..state import PitBoxState
from ..tools import get_tools


async def execute_tools(state: PitBoxState) -> Dict[str, Any]:
    """Execute async tools from the last message's tool calls."""
    last_message = state["messages"][-1]
    
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {"messages": []}
    
    tools = get_tools()
    tool_map = {tool.name: tool for tool in tools}
    
    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        
        if tool_name not in tool_map:
            tool_messages.append(
                ToolMessage(
                    content=f"Tool {tool_name} not found",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
            )
            continue
        
        tool = tool_map[tool_name]
        
        try:
            # Try async invocation first (for MCP tools)
            if hasattr(tool, "ainvoke"):
                result = await tool.ainvoke(tool_args)
            else:
                # Fallback to sync invocation
                result = tool.invoke(tool_args)
            
            # Convert result to string if needed
            if isinstance(result, dict):
                import json
                content = json.dumps(result)
            else:
                content = str(result)
            
            tool_messages.append(
                ToolMessage(
                    content=content,
                    tool_call_id=tool_id,
                    name=tool_name,
                )
            )
        except Exception as e:
            tool_messages.append(
                ToolMessage(
                    content=f"Error executing tool: {str(e)}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
            )
    
    return {"messages": tool_messages}


def call_model(state: PitBoxState) -> Dict[str, Any]:
    """Main agent node - processes user query and decides on tool usage."""
    model = get_chat_model()
    tools = get_tools()
    model_with_tools = model.bind_tools(tools)

    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: PitBoxState) -> Literal["action", "__end__"]:
    """Determine if we need to call tools or can end the conversation."""
    last_message = state["messages"][-1]

    # If the last message has tool calls, route to tool execution
    if getattr(last_message, "tool_calls", None):
        return "action"

    # Otherwise, we're done
    return END


@lru_cache(maxsize=1)
def build_graph() -> StateGraph:
    """Build the simple pit box agent graph."""
    # Initialize the graph
    graph = StateGraph(PitBoxState)

    # Add nodes
    graph.add_node("agent", call_model)
    graph.add_node("action", execute_tools)  # Use our custom async tool executor

    # Set entry point
    graph.set_entry_point("agent")

    # Add routing logic
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "action": "action",
            "__end__": END,
        },
    )

    # Tools always route back to agent
    graph.add_edge("action", "agent")

    return graph


# Compile the graph for export
graph = build_graph().compile()
