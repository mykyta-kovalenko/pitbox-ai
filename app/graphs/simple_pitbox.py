"""Simple NASCAR Pit Box Agent - Basic Q&A with tool routing"""
from typing import Dict, Any, Literal
from functools import lru_cache

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage

from ..state import PitBoxState
from ..models import get_chat_model
from ..tools import get_tools


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
    graph.add_node("action", ToolNode(get_tools()))
    
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
