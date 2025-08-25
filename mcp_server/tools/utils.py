"""Common utilities for MCP tools."""

import os
from typing import Any, Optional

import httpx
from pydantic import BaseModel

# Configuration
WEB_SERVER_URL = os.getenv("WEB_SERVER_URL", "http://localhost:5000")
API_TIMEOUT = 30


class APIResponse(BaseModel):
    """Standard API response model."""

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


async def make_api_request(endpoint: str, method: str = "GET") -> APIResponse:
    """Make a request to the TrackHouse web server API."""
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            url = f"{WEB_SERVER_URL}{endpoint}"
            response = await client.request(method, url)
            response.raise_for_status()

            # Handle different response types
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                data = response.json()
            else:
                data = response.text

            return APIResponse(success=True, data=data)
    except httpx.HTTPStatusError as e:
        return APIResponse(
            success=False, error=f"HTTP {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))
