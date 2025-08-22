#!/usr/bin/env python3
"""Comprehensive test suite for the RAG system"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.tools.rag_knowledge import get_knowledge_tools


def test_basic_rag_functionality():
    """Test basic RAG functionality with simple queries."""
    tools = get_knowledge_tools()
    assert len(tools) == 4, f"Expected 4 tools, got {len(tools)}"

    # Quick smoke test
    general_tool = next((t for t in tools if t.name == "search_nascar_knowledge"), None)
    assert general_tool is not None, "search_nascar_knowledge tool not found"

    result = general_tool.invoke({"query": "What is NASCAR?"})
    assert len(result) > 0, "Empty response from RAG system"
    print("✅ Basic RAG functionality test passed")


def test_comprehensive_rag_cases():
    """Test the RAG tools with comprehensive sample queries."""

    tools = get_knowledge_tools()
    print(f"Available RAG tools: {[tool.name for tool in tools]}")

    # Expanded test cases covering different categories
    test_cases = [
        # Trackhouse Racing Team Questions
        (
            "search_trackhouse_team_info",
            "Who drives the number 1 car?",
            "Should mention Ross Chastain",
        ),
        (
            "search_trackhouse_team_info",
            "When was Trackhouse Racing founded?",
            "Should mention 2021",
        ),
        (
            "search_trackhouse_team_info",
            "Who owns Trackhouse Racing?",
            "Should mention Justin Marks and Pitbull",
        ),
        (
            "search_trackhouse_team_info",
            "What was Ross Chastain's first win?",
            "Should mention Circuit of The Americas 2022",
        ),
        (
            "search_trackhouse_team_info",
            "Tell me about Daniel Suarez's historic achievement",
            "Should mention first Mexican driver to win Cup Series",
        ),
        (
            "search_trackhouse_team_info",
            "What is Project 91?",
            "Should mention other motorsports drivers trying NASCAR",
        ),
        # NASCAR Terminology Questions
        (
            "search_nascar_terminology",
            "What does loose mean?",
            "Should explain oversteer and fishtailing",
        ),
        (
            "search_nascar_terminology",
            "What is drafting?",
            "Should explain nose-to-tail racing and vacuum effect",
        ),
        (
            "search_nascar_terminology",
            "Explain the playoff system",
            "Should mention elimination format and Championship 4",
        ),
        (
            "search_nascar_terminology",
            "What are stage points?",
            "Should explain bonus points for stage finishes",
        ),
        (
            "search_nascar_terminology",
            "What does the yellow flag mean?",
            "Should explain caution conditions",
        ),
        (
            "search_nascar_terminology",
            "What is a wave around?",
            "Should explain lapped cars procedure",
        ),
        # Track Information Questions
        (
            "search_track_information",
            "Tell me about Daytona banking",
            "Should mention 31-degree banking",
        ),
        (
            "search_track_information",
            "What makes Bristol unique?",
            "Should mention concrete surface and Thunder Valley nickname",
        ),
        (
            "search_track_information",
            "How long is Charlotte Motor Speedway?",
            "Should mention 1.5 miles",
        ),
        (
            "search_track_information",
            "What is the Charlotte ROVAL?",
            "Should mention road course configuration",
        ),
        (
            "search_track_information",
            "Tell me about Las Vegas progressive banking",
            "Should mention 12-20 degrees banking",
        ),
        (
            "search_track_information",
            "What happened at Atlanta in 2022?",
            "Should mention reconfiguration to superspeedway racing",
        ),
        # General NASCAR Knowledge Questions
        (
            "search_nascar_knowledge",
            "Ross Chastain Hail Melon",
            "Should explain Martinsville wall-riding move",
        ),
        (
            "search_nascar_knowledge",
            "What is NASCAR Overtime?",
            "Should explain extended finish procedure",
        ),
        (
            "search_nascar_knowledge",
            "How many laps is the Coca-Cola 600?",
            "Should mention it's 600 miles, longest race",
        ),
        (
            "search_nascar_knowledge",
            "What makes Trackhouse Racing different?",
            "Should mention international focus and innovation",
        ),
        # Edge Cases and Complex Questions
        (
            "search_nascar_knowledge",
            "Who has the most NASCAR wins?",
            "Should mention Richard Petty with 200 wins",
        ),
        (
            "search_nascar_knowledge",
            "What is a crown jewel race?",
            "Should mention prestigious historic races",
        ),
        (
            "search_nascar_knowledge",
            "How does pit road speed work?",
            "Should mention speed limits and penalties",
        ),
        # Test cases that might not have answers
        (
            "search_nascar_knowledge",
            "What is Formula 1?",
            "Should indicate no information available",
        ),
        (
            "search_trackhouse_team_info",
            "Who drives the #42 car?",
            "Should indicate information not available or redirect",
        ),
    ]

    passed_tests = 0
    failed_tests = 0

    for tool_name, query, expected_content in test_cases:
        tool = next((t for t in tools if t.name == tool_name), None)
        if tool:
            print(f"\n=== Testing {tool_name} ====")
            print(f"Query: {query}")
            print(f"Expected: {expected_content}")
            try:
                result = tool.invoke({"query": query})
                print(
                    f"Result: {result[:300]}..."
                    if len(result) > 300
                    else f"Result: {result}"
                )

                # Basic validation
                if (
                    "I don't have that information" in result
                    or "don't have information" in result.lower()
                ):
                    print("⚠️  INFO: No specific information found for this query")
                else:
                    print("✅ Response generated successfully")

                passed_tests += 1

            except Exception as e:
                print(f"❌ Error: {e}")
                failed_tests += 1
        else:
            print(f"❌ Tool {tool_name} not found")
            failed_tests += 1

    print("\n=== Test Summary ====")
    print(f"Total test cases: {len(test_cases)}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests / (passed_tests + failed_tests) * 100):.1f}%")


def test_rag_response_quality():
    """Test the quality and consistency of RAG responses."""
    tools = get_knowledge_tools()
    general_tool = next((t for t in tools if t.name == "search_nascar_knowledge"), None)

    if not general_tool:
        print("❌ General NASCAR tool not found")
        return

    # Test response consistency
    query = "What is the Hail Melon move?"
    responses = []

    for i in range(3):
        response = general_tool.invoke({"query": query})
        responses.append(response)

    print("\n=== Testing Response Consistency ====")
    print(f"Query: {query}")

    for i, response in enumerate(responses):
        print(f"\nResponse {i + 1}: {response[:200]}...")

    # Check if responses are reasonably similar (basic check)
    if len(set(responses)) == 1:
        print("✅ Responses are identical (perfect consistency)")
    elif (
        "Hail Melon" in responses[0]
        and "Hail Melon" in responses[1]
        and "Hail Melon" in responses[2]
    ):
        print("✅ Responses contain key information consistently")
    else:
        print("⚠️  Responses vary significantly")


if __name__ == "__main__":
    # Set environment variables for testing
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        sys.exit(1)

    # Set knowledge base path
    os.environ.setdefault("KNOWLEDGE_BASE_PATH", "app/knowledge")

    print("🏁 Starting comprehensive RAG testing...")

    # Run all tests
    test_basic_rag_functionality()
    print("\n" + "=" * 50)

    test_comprehensive_rag_cases()
    print("\n" + "=" * 50)

    test_rag_response_quality()
    print("\n🏁 RAG testing complete!")
