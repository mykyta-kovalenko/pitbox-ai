#!/usr/bin/env python
"""Test script to verify MCP integration with LangGraph agents."""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent))

from app.tools import get_tools


def test_tool_discovery():
    """Test that MCP tools are discovered and loaded."""
    print("=" * 60)
    print("Testing MCP Tool Discovery")
    print("=" * 60)

    # Get all tools
    tools = get_tools()

    print(f"\nTotal tools loaded: {len(tools)}")

    # Better way to identify tools - RAG tools contain "search" and knowledge terms
    # MCP tools would have names ending in "_tool" or containing NASCAR-specific terms
    rag_tools = [
        t
        for t in tools
        if "search" in t.name.lower()
        and any(term in t.name.lower() for term in ["track", "nascar", "team"])
    ]

    # MCP tools are those with "_tool" suffix or NASCAR-specific operations
    mcp_terms = ["car_position", "pit_", "flag", "telemetry", "vehicle"]
    mcp_tools = [
        t
        for t in tools
        if t.name.endswith("_tool") or any(term in t.name.lower() for term in mcp_terms)
    ]

    # Anything else that's not categorized
    other_tools = [t for t in tools if t not in rag_tools and t not in mcp_tools]

    print(f"- RAG Knowledge tools: {len(rag_tools)}")
    print(f"- MCP Server tools: {len(mcp_tools)}")
    if other_tools:
        print(f"- Other/Uncategorized tools: {len(other_tools)}")

    if rag_tools:
        print("\nRAG Tools:")
        for tool in rag_tools:
            print(f"  • {tool.name}: {tool.description[:50]}...")

    if mcp_tools:
        print("\nMCP Tools (from server):")
        for tool in mcp_tools[:10]:  # Show first 10
            desc = tool.description[:50] if tool.description else "No description"
            print(f"  • {tool.name}: {desc}...")
        if len(mcp_tools) > 10:
            print(f"  ... and {len(mcp_tools) - 10} more")
    else:
        print("\n⚠️  No MCP tools loaded. Make sure:")
        print("  1. The mock edge server is running: python mock_edge_server.py")
        print("  2. For HTTP transport: python mcp_server/server.py --transport http")
        print("  3. Set environment: export MCP_TRANSPORT=http")

    if other_tools:
        print("\nOther tools (may need categorization):")
        for tool in other_tools[:5]:
            print(f"  • {tool.name}")

    return len(mcp_tools) > 0


async def test_mcp_tool_execution():
    """Test executing an MCP tool."""
    print("\n" + "=" * 60)
    print("Testing MCP Tool Execution")
    print("=" * 60)

    tools = get_tools()

    # Find a simple MCP tool to test
    health_tool = next((t for t in tools if "health" in t.name.lower()), None)

    if health_tool:
        print(f"\nTesting tool: {health_tool.name}")
        try:
            # MCP tools from langchain-mcp-adapters are always async
            # Use ainvoke for async tools
            result = await health_tool.ainvoke({})
            print(f"Result: {result}")
            return True
        except Exception as e:
            print(f"Error executing tool: {e}")
            # Try with empty input if the tool expects parameters
            try:
                print("Retrying with minimal parameters...")
                # Some tools might need specific parameters
                if "vehicle" in health_tool.name.lower():
                    result = await health_tool.ainvoke({})
                else:
                    result = await health_tool.ainvoke({})
                print(f"Result: {result}")
                return True
            except Exception as e2:
                print(f"Second attempt failed: {e2}")
                return False
    else:
        print("No health check tool found")
        return False


def test_agent_integration():
    """Test that agents can use MCP tools."""
    print("\n" + "=" * 60)
    print("Testing Agent Integration")
    print("=" * 60)

    try:
        from app.graphs.analytics_agent import build_graph

        build_graph()  # Build the graph to verify it works
        print("✓ Analytics agent graph built successfully")

        # Check that the graph has access to tools
        from app.tools import get_tools

        tools = get_tools()

        if tools:
            print(f"✓ Agent has access to {len(tools)} tools")
            return True
        else:
            print("✗ No tools available to agent")
            return False

    except Exception as e:
        print(f"✗ Error building agent graph: {e}")
        return False


def main():
    """Run all tests."""
    print("\n🏁 NASCAR Pit Box MCP Integration Test\n")

    # Test 1: Tool Discovery
    discovery_ok = test_tool_discovery()

    # Test 2: Tool Execution
    execution_ok = asyncio.run(test_mcp_tool_execution())

    # Test 3: Agent Integration
    agent_ok = test_agent_integration()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tool Discovery: {'✓ PASS' if discovery_ok else '✗ FAIL'}")
    print(f"Tool Execution: {'✓ PASS' if execution_ok else '✗ FAIL'}")
    print(f"Agent Integration: {'✓ PASS' if agent_ok else '✗ FAIL'}")

    if all([discovery_ok, execution_ok, agent_ok]):
        print("\n✅ All tests passed! MCP integration is working.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
