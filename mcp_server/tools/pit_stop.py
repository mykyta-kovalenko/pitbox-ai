"""Pit stop and tire management tools."""

from typing import Any, Dict, Optional

from pydantic import Field

from .utils import make_api_request


async def get_pit_events(car_number: str = Field(description="Car number")) -> Dict[str, Any]:
    """Get pit entry and exit events for a specific car.
    
    Args:
        car_number: The car number to query
        
    Returns lists of pit in and pit out lap numbers.
    """
    result = await make_api_request(f"/api/pit/{car_number}")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_pit_times(
    car_number: str = Field(description="Car number"),
    lap_number: Optional[int] = Field(default=None, description="Specific lap number")
) -> Dict[str, Any]:
    """Get pit stop duration data for a specific car.
    
    Args:
        car_number: The car number to query
        lap_number: Optional specific lap number
        
    Returns pit stop time information.
    """
    if lap_number:
        result = await make_api_request(f"/api/pt/{car_number}/{lap_number}")
    else:
        result = await make_api_request(f"/api/pt/{car_number}")
    
    if result.success:
        return {"car": car_number, "pit_times": result.data}
    return {"error": result.error}


async def get_tire_data(
    lap_number: int = Field(description="Lap number"),
    car_number: Optional[str] = Field(default=None, description="Car number")
) -> Dict[str, Any]:
    """Get tire data for a specific lap, optionally for a specific car.
    
    Args:
        lap_number: The lap number to query
        car_number: Optional car number (if not provided, returns all cars)
        
    Returns tire information for the specified lap.
    """
    if car_number:
        result = await make_api_request(f"/api/tires/{lap_number}/{car_number}")
    else:
        result = await make_api_request(f"/api/tires/{lap_number}")
    
    if result.success:
        return {"lap": lap_number, "tires": result.data}
    return {"error": result.error}