"""Race analysis and comparison tools."""

from typing import Any, Dict

from pydantic import Field

from .car_data import get_all_positions, get_lap_time
from .pit_stop import get_pit_events, get_pit_times
from .race_status import get_all_laps


async def analyze_race_leader() -> Dict[str, Any]:
    """Analyze who is currently leading the race and by how much.
    
    Returns leader information and gap to second place.
    """
    positions = await get_all_positions()
    laps = await get_all_laps()
    
    if "error" in positions or "error" in laps:
        return {"error": "Could not fetch race data"}
    
    # Find the leader (position 1)
    leader_car = None
    for car, pos in positions.items() if isinstance(positions, dict) else []:
        if str(pos) == "1":
            leader_car = car
            break
    
    if not leader_car:
        return {"error": "No leader found"}
    
    # Get leader's lap count
    leader_lap = laps.get(leader_car, 0) if isinstance(laps, dict) else 0
    
    # Find second place
    second_car = None
    for car, pos in positions.items() if isinstance(positions, dict) else []:
        if str(pos) == "2":
            second_car = car
            break
    
    result = {
        "leader": leader_car,
        "position": 1,
        "lap": leader_lap
    }
    
    if second_car:
        second_lap = laps.get(second_car, 0) if isinstance(laps, dict) else 0
        result["second_place"] = second_car
        result["gap_laps"] = int(leader_lap) - int(second_lap) if leader_lap and second_lap else 0
    
    return result


async def analyze_pit_strategy(car_number: str = Field(description="Car number")) -> Dict[str, Any]:
    """Analyze pit stop strategy for a specific car.
    
    Args:
        car_number: The car number to analyze
        
    Returns pit stop patterns and statistics.
    """
    pit_events = await get_pit_events(car_number)
    pit_times = await get_pit_times(car_number)
    
    if "error" in pit_events:
        return pit_events
    
    pit_data = pit_events if isinstance(pit_events, dict) else {}
    
    analysis = {
        "car": car_number,
        "total_stops": len(pit_data.get("in", [])),
        "pit_in_laps": pit_data.get("in", []),
        "pit_out_laps": pit_data.get("out", [])
    }
    
    if not isinstance(pit_times, dict) or "error" not in pit_times:
        times_data = pit_times.get("pit_times", {}) if isinstance(pit_times, dict) else {}
        if times_data:
            analysis["pit_durations"] = times_data
            if isinstance(times_data, dict) and times_data:
                durations = [float(v) for v in times_data.values() if v]
                if durations:
                    analysis["average_pit_time"] = sum(durations) / len(durations)
    
    return analysis


async def compare_lap_times(
    car1: str = Field(description="First car number"),
    car2: str = Field(description="Second car number")
) -> Dict[str, Any]:
    """Compare lap times between two cars.
    
    Args:
        car1: First car number to compare
        car2: Second car number to compare
        
    Returns comparison of lap times and performance metrics.
    """
    car1_times = await get_lap_time(car1)
    car2_times = await get_lap_time(car2)
    
    if "error" in car1_times or "error" in car2_times:
        return {"error": "Could not fetch lap times for comparison"}
    
    car1_data = car1_times.get("lap_times", {})
    car2_data = car2_times.get("lap_times", {})
    
    comparison = {
        "car1": car1,
        "car2": car2,
        "car1_laps": len(car1_data) if isinstance(car1_data, dict) else 0,
        "car2_laps": len(car2_data) if isinstance(car2_data, dict) else 0
    }
    
    # Calculate averages if data is available
    if isinstance(car1_data, dict) and car1_data:
        times1 = [float(v) for v in car1_data.values() if v]
        if times1:
            comparison["car1_average"] = sum(times1) / len(times1)
            comparison["car1_best"] = min(times1)
    
    if isinstance(car2_data, dict) and car2_data:
        times2 = [float(v) for v in car2_data.values() if v]
        if times2:
            comparison["car2_average"] = sum(times2) / len(times2)
            comparison["car2_best"] = min(times2)
    
    return comparison