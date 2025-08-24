"""TrackHouse MCP tools package."""

# System status tools
from .system_status import check_system_health, get_vehicle_id

# Car data tools
from .car_data import (
    get_all_positions,
    get_average_lap_time,
    get_best_lap_time,
    get_car_position,
    get_car_rank,
    get_lap_time,
)

# Pit stop tools
from .pit_stop import get_pit_events, get_pit_times, get_tire_data

# Race status tools
from .race_status import (
    get_all_flags,
    get_all_laps,
    get_current_flag,
    get_current_lap,
    get_starting_grid,
    get_track_info,
)

# Content tools
from .content import get_all_drivers, get_driver_info, get_team_info

# Telemetry tools
from .telemetry import get_telemetry_channels

# Analysis tools
from .analysis import analyze_pit_strategy, analyze_race_leader, compare_lap_times

__all__ = [
    # System status
    "check_system_health",
    "get_vehicle_id",
    # Car data
    "get_car_position",
    "get_all_positions",
    "get_car_rank",
    "get_lap_time",
    "get_best_lap_time",
    "get_average_lap_time",
    # Pit stops
    "get_pit_events",
    "get_pit_times",
    "get_tire_data",
    # Race status
    "get_current_flag",
    "get_all_flags",
    "get_current_lap",
    "get_all_laps",
    "get_starting_grid",
    "get_track_info",
    # Content
    "get_driver_info",
    "get_all_drivers",
    "get_team_info",
    # Telemetry
    "get_telemetry_channels",
    # Analysis
    "analyze_race_leader",
    "analyze_pit_strategy",
    "compare_lap_times",
]