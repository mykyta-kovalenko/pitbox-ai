#!/usr/bin/env python
"""FastAPI server to expose the NASCAR Pit Box Agent as an API."""

import os
import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
import json
import uvicorn

from app.graphs.simple_pitbox import graph


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


app = FastAPI(title="NASCAR Pit Box AI API", version="1.0.0")

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "NASCAR Pit Box AI API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send a message to the NASCAR AI agent",
            "/chat/stream": "POST - Stream responses from the NASCAR AI agent",
            "/health": "GET - Check API health status"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "pitbox-ai-api"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the NASCAR Pit Box Agent and get a response."""
    try:
        # Invoke the graph with the user's message
        result = await graph.ainvoke({
            "messages": [HumanMessage(content=request.message)]
        })
        
        # Get the final message (should be the AI's response)
        final_message = result["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            return ChatResponse(response=final_message.content)
        else:
            raise HTTPException(status_code=500, detail="Unexpected response type from agent")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_stream(message: str):
    """Generate streaming response from the agent."""
    try:
        # For now, we'll send the complete response as a single chunk
        # In a production system, you'd want to implement true streaming
        result = await graph.ainvoke({
            "messages": [HumanMessage(content=message)]
        })
        
        final_message = result["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            # Send as Server-Sent Events format
            data = json.dumps({"content": final_message.content})
            yield f"data: {data}\n\n"
            yield f"data: [DONE]\n\n"
        else:
            error_data = json.dumps({"error": "Unexpected response type"})
            yield f"data: {error_data}\n\n"
            
    except Exception as e:
        error_data = json.dumps({"error": str(e)})
        yield f"data: {error_data}\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream responses from the NASCAR Pit Box Agent."""
    return StreamingResponse(
        generate_stream(request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


if __name__ == "__main__":
    print("🏁 Starting NASCAR Pit Box AI API Server")
    print("=" * 60)
    print("Server running at: http://localhost:8765")
    print("API documentation: http://localhost:8765/docs")
    print("=" * 60)
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
    
    # Run the server without reload to avoid the import string issue
    uvicorn.run(app, host="0.0.0.0", port=8765)