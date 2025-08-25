"""Race status and track information tools."""

from typing import Any, Dict, Optional

from pydantic import Field

from .utils import make_api_request


async def get_current_flag() -> Dict[str, str]:
    """Get the current flag status of the race.

    Returns the current flag (green, yellow, red, white, checkered).
    """
    result = await make_api_request("/api/flag")
    if result.success:
        return {"flag": result.data}
    return {"error": result.error}


async def get_all_flags() -> Dict[str, Any]:
    """Get all flag events that have occurred during the race.

    Returns a dictionary of all flag changes with timestamps.
    """
    result = await make_api_request("/api/flags")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_current_lap() -> Dict[str, Any]:
    """Get the current lap number for the race leader.

    Returns the leader's current lap number.
    """
    result = await make_api_request("/api/lap")
    if result.success:
        return {"current_lap": result.data}
    return {"error": result.error}


async def get_all_laps() -> Dict[str, Any]:
    """Get current lap count for all cars in the race.

    Returns a dictionary mapping car numbers to their current lap counts.
    """
    result = await make_api_request("/api/laps")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_starting_grid(
    car_number: Optional[str] = Field(default=None, description="Car number"),
) -> Dict[str, Any]:
    """Get the starting grid positions.

    Args:
        car_number: Optional car number (if not provided, returns all positions)

    Returns starting grid position(s).
    """
    if car_number:
        result = await make_api_request(f"/api/grid/{car_number}")
    else:
        result = await make_api_request("/api/grid")

    if result.success:
        return {"grid": result.data}
    return {"error": result.error}


async def get_track_info(
    car_number: str = Field(description="Car number"),
) -> Dict[str, Any]:
    """Get track information including layout and configuration.

    Args:
        car_number: The car number (used for context)

    Returns track data including SVG paths for visualization.
    """
    result = await make_api_request(f"/api/track/{car_number}")
    if result.success:
        return result.data
    return {"error": result.error}
