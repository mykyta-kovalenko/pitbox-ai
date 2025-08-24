"""Car data and performance tools."""

from typing import Any, Dict, Optional

from pydantic import Field

from .utils import make_api_request


async def get_car_position(car_number: str = Field(description="Car number (e.g., '1', '88', '99')")) -> Dict[str, Any]:
    """Get the current position for a specific car in the race.
    
    Args:
        car_number: The car number to query
        
    Returns current position/rank information for the car.
    """
    result = await make_api_request(f"/api/pos/{car_number}")
    if result.success:
        return {"car": car_number, "position": result.data}
    return {"error": result.error}


async def get_all_positions() -> Dict[str, Any]:
    """Get current positions for all cars in the race.
    
    Returns a dictionary mapping car numbers to their positions.
    """
    result = await make_api_request("/api/pos")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_car_rank(car_number: str = Field(description="Car number")) -> Dict[str, Any]:
    """Get detailed ranking information for a specific car.
    
    Args:
        car_number: The car number to query
        
    Returns rank data including ordinal position (1st, 2nd, etc).
    """
    result = await make_api_request(f"/api/rank/{car_number}")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_lap_time(
    car_number: str = Field(description="Car number"),
    lap_number: Optional[int] = Field(default=None, description="Specific lap number")
) -> Dict[str, Any]:
    """Get lap time data for a specific car.
    
    Args:
        car_number: The car number to query
        lap_number: Optional specific lap number (if not provided, returns all laps)
        
    Returns lap time(s) for the specified car.
    """
    if lap_number:
        result = await make_api_request(f"/api/lt/{car_number}/{lap_number}")
    else:
        result = await make_api_request(f"/api/lt/{car_number}")
    
    if result.success:
        return {"car": car_number, "lap_times": result.data}
    return {"error": result.error}


async def get_best_lap_time(car_number: Optional[str] = Field(default=None, description="Car number")) -> Dict[str, Any]:
    """Get the best lap time for a specific car or the overall best.
    
    Args:
        car_number: Optional car number (if not provided, returns overall best)
        
    Returns the best lap time information.
    """
    if car_number:
        result = await make_api_request(f"/api/bt/{car_number}")
    else:
        result = await make_api_request("/api/bt")
    
    if result.success:
        return {"best_time": result.data}
    return {"error": result.error}


async def get_average_lap_time(
    car_number: str = Field(description="Car number"),
    lap_number: Optional[int] = Field(default=None, description="Specific lap number")
) -> Dict[str, Any]:
    """Get average lap time data for a specific car.
    
    Args:
        car_number: The car number to query
        lap_number: Optional specific lap number
        
    Returns average lap time information.
    """
    if lap_number:
        result = await make_api_request(f"/api/at/{car_number}/{lap_number}")
    else:
        result = await make_api_request(f"/api/at/{car_number}")
    
    if result.success:
        return {"car": car_number, "average_times": result.data}
    return {"error": result.error}