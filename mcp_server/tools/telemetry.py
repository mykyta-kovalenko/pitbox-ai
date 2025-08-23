"""Telemetry data tools."""

from typing import Dict, List


async def get_telemetry_channels() -> Dict[str, List[str]]:
    """Get list of available telemetry channels.
    
    Returns available telemetry data channels that can be queried.
    """
    # This would connect to real telemetry endpoints when available
    return {
        "channels": [
            "speed", "throttle", "brake", "steering",
            "rpm", "gear", "lap_fraction", "lap_distance"
        ],
        "note": "Real-time telemetry requires WebSocket connection"
    }