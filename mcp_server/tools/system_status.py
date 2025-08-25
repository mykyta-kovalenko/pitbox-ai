"""System status monitoring tools."""

from typing import Any, Dict

from .utils import make_api_request


async def check_system_health() -> Dict[str, Any]:
    """Check the health status of the TrackHouse system including all services.

    Returns the status of web server, Redis connections, and available services.
    """
    result = await make_api_request("/health")
    if result.success:
        return {"status": "healthy", "services": result.data}
    return {"status": "unhealthy", "error": result.error}


async def get_vehicle_id() -> Dict[str, str]:
    """Get the current vehicle ID being monitored.

    Returns the vehicle/car ID that this edge server is configured for.
    """
    result = await make_api_request("/api/vehicle_id")
    if result.success:
        return result.data
    return {"error": result.error}
