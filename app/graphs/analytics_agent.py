"""Advanced NASCAR Analytics Agent - Multi-step analysis with evaluation loop"""
from typing import Dict, Any, Literal
from functools import lru_cache

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage

from ..state import PitBoxState
from ..models import get_chat_model
from ..tools import get_tools


def analyze_query(state: PitBoxState) -> Dict[str, Any]:
    """Analyze complex NASCAR queries and plan multi-step data collection."""
    model = get_chat_model()
    tools = get_tools()
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = """
    You are an advanced NASCAR analytics agent. For complex queries requiring multiple data points:
    1. Break down the analysis into steps
    2. Identify required data sources (lap times, pit stops, positions, etc.)
    3. Call appropriate tools to gather data
    4. Perform calculations and trend analysis
    
    Focus on actionable insights, not just raw data.
    """
    
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    response = model_with_tools.invoke(messages)
    
    return {"messages": [response]}


def evaluate_response(state: PitBoxState) -> Dict[str, Any]:
    """Evaluate if the analysis is complete and accurate."""
    # Simple loop protection - limit message count
    if len(state["messages"]) > 10:
        return {
            "messages": [
                AIMessage(content="Analysis complete. Let me know if you need more details.")
            ]
        }
    
    # For now, just pass through - could add quality checks later
    return {"messages": []}


def should_continue_analysis(state: PitBoxState) -> Literal["action", "evaluate", "__end__"]:
    """Route based on current state - tools, evaluation, or completion."""
    last_message = state["messages"][-1]
    
    # If we have tool calls, execute them
    if getattr(last_message, "tool_calls", None):
        return "action"
    
    # If we've done enough back and forth, end
    if len(state["messages"]) > 8:
        return END
    
    # Check if we should evaluate the response
    # For now, simple heuristic based on content
    content = getattr(last_message, "content", "")
    if "analysis" in content.lower() or "trend" in content.lower():
        return "evaluate"
    
    return END


def should_refine_or_complete(state: PitBoxState) -> Literal["agent", "__end__"]:
    """After evaluation, decide if we need more analysis or we're done."""
    # Simple completion logic - could be enhanced
    if len(state["messages"]) > 10:
        return END
    
    # For now, typically complete after evaluation
    return END


@lru_cache(maxsize=1)
def build_graph() -> StateGraph:
    """Build the analytics agent graph with evaluation loop."""
    # Initialize the graph
    graph = StateGraph(PitBoxState)
    
    # Add nodes
    graph.add_node("agent", analyze_query)
    graph.add_node("action", ToolNode(get_tools()))
    graph.add_node("evaluate", evaluate_response)
    
    # Set entry point
    graph.set_entry_point("agent")
    
    # Add routing from agent
    graph.add_conditional_edges(
        "agent",
        should_continue_analysis,
        {
            "action": "action",
            "evaluate": "evaluate", 
            "__end__": END,
        },
    )
    
    # Tools route back to agent
    graph.add_edge("action", "agent")
    
    # Evaluation routing
    graph.add_conditional_edges(
        "evaluate",
        should_refine_or_complete,
        {
            "agent": "agent",
            "__end__": END,
        },
    )
    
    return graph


# Compile the graph for export
graph = build_graph().compile()
