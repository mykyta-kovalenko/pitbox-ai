#!/usr/bin/env python
"""CLI runner for the NASCAR Pit Box Agent."""

import asyncio
import sys
from langchain_core.messages import HumanMessage, AIMessage
from app.graphs.simple_pitbox import graph


async def main():
    """Run the simple pitbox agent with a question from command line."""
    
    # Get the question from command line arguments or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        print("Usage: python run_pitbox.py <your question>")
        print("Example: python run_pitbox.py What is NASCAR?")
        print("\nUsing default question: What is NASCAR?")
        question = "What is NASCAR?"
    
    print(f"\n🏁 NASCAR Pit Box Agent")
    print("=" * 60)
    print(f"Question: {question}")
    print("=" * 60)
    print("\nThinking...\n")
    
    try:
        # Invoke the graph with the user's question (async)
        result = await graph.ainvoke({
            "messages": [HumanMessage(content=question)]
        })
        
        # Get the final message (should be the AI's response)
        final_message = result["messages"][-1]
        
        # Print the response
        if isinstance(final_message, AIMessage):
            print("Answer:")
            print("-" * 60)
            print(final_message.content)
        else:
            print("Unexpected response type:", type(final_message))
            print(final_message)
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. You have set OPENAI_API_KEY environment variable")
        print("2. The mock edge server is running: uv run python mock_edge_server.py")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())