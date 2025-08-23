"""Driver and team content tools."""

from typing import Any, Dict

from pydantic import Field

from .utils import make_api_request


async def get_driver_info(car_number: str = Field(description="Car number")) -> Dict[str, Any]:
    """Get driver information for a specific car.
    
    Args:
        car_number: The car number to query
        
    Returns driver details including name, team, and other information.
    """
    result = await make_api_request(f"/content/{car_number}")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_all_drivers() -> Dict[str, Any]:
    """Get information about all drivers in the race.
    
    Returns a dictionary of all drivers with their car numbers and details.
    """
    result = await make_api_request("/content")
    if result.success:
        return result.data
    return {"error": result.error}


async def get_team_info(car_number: str = Field(description="Car number")) -> Dict[str, Any]:
    """Get team information for a specific car.
    
    Args:
        car_number: The car number to query
        
    Returns team details including crew members and sponsors.
    """
    result = await make_api_request(f"/content/{car_number}")
    if result.success:
        data = result.data
        if isinstance(data, dict):
            return {
                "car": car_number,
                "team": data.get("team", ""),
                "crew": data.get("crew", []),
                "sponsors": data.get("sponsors", [])
            }
        return {"car": car_number, "data": data}
    return {"error": result.error}