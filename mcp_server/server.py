"""TrackHouse MCP Server - Integrated with edge_server/web_server."""

import asyncio
import sys
from pathlib import Path

from fastmcp import FastMCP

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import all tools
from tools import (
    analyze_pit_strategy,
    analyze_race_leader,
    check_system_health,
    compare_lap_times,
    get_all_drivers,
    get_all_flags,
    get_all_laps,
    get_all_positions,
    get_average_lap_time,
    get_best_lap_time,
    get_car_position,
    get_car_rank,
    get_current_flag,
    get_current_lap,
    get_driver_info,
    get_lap_time,
    get_pit_events,
    get_pit_times,
    get_starting_grid,
    get_team_info,
    get_telemetry_channels,
    get_tire_data,
    get_track_info,
    get_vehicle_id,
)
from tools.utils import WEB_SERVER_URL

# Initialize FastMCP server
mcp = FastMCP("TrackHouse Racing System")


# Register all tools with the MCP server
# System Status Tools
@mcp.tool()
async def check_system_health_tool():
    """Check the health status of the TrackHouse system including all services."""
    return await check_system_health()


@mcp.tool()
async def get_vehicle_id_tool():
    """Get the current vehicle ID being monitored."""
    return await get_vehicle_id()


# Car Data Tools
@mcp.tool()
async def get_car_position_tool(car_number: str):
    """Get the current position for a specific car in the race."""
    return await get_car_position(car_number)


@mcp.tool()
async def get_all_positions_tool():
    """Get current positions for all cars in the race."""
    return await get_all_positions()


@mcp.tool()
async def get_car_rank_tool(car_number: str):
    """Get detailed ranking information for a specific car."""
    return await get_car_rank(car_number)


@mcp.tool()
async def get_lap_time_tool(car_number: str, lap_number: int = None):
    """Get lap time data for a specific car."""
    return await get_lap_time(car_number, lap_number)


@mcp.tool()
async def get_best_lap_time_tool(car_number: str = None):
    """Get the best lap time for a specific car or the overall best."""
    return await get_best_lap_time(car_number)


@mcp.tool()
async def get_average_lap_time_tool(car_number: str, lap_number: int = None):
    """Get average lap time data for a specific car."""
    return await get_average_lap_time(car_number, lap_number)


# Pit Stop Tools
@mcp.tool()
async def get_pit_events_tool(car_number: str):
    """Get pit entry and exit events for a specific car."""
    return await get_pit_events(car_number)


@mcp.tool()
async def get_pit_times_tool(car_number: str, lap_number: int = None):
    """Get pit stop duration data for a specific car."""
    return await get_pit_times(car_number, lap_number)


@mcp.tool()
async def get_tire_data_tool(lap_number: int, car_number: str = None):
    """Get tire data for a specific lap, optionally for a specific car."""
    return await get_tire_data(lap_number, car_number)


# Race Status Tools
@mcp.tool()
async def get_current_flag_tool():
    """Get the current flag status of the race."""
    return await get_current_flag()


@mcp.tool()
async def get_all_flags_tool():
    """Get all flag events that have occurred during the race."""
    return await get_all_flags()


@mcp.tool()
async def get_current_lap_tool():
    """Get the current lap number for the race leader."""
    return await get_current_lap()


@mcp.tool()
async def get_all_laps_tool():
    """Get current lap count for all cars in the race."""
    return await get_all_laps()


@mcp.tool()
async def get_starting_grid_tool(car_number: str = None):
    """Get the starting grid positions."""
    return await get_starting_grid(car_number)


@mcp.tool()
async def get_track_info_tool(car_number: str):
    """Get track information including layout and configuration."""
    return await get_track_info(car_number)


# Content Tools
@mcp.tool()
async def get_driver_info_tool(car_number: str):
    """Get driver information for a specific car."""
    return await get_driver_info(car_number)


@mcp.tool()
async def get_all_drivers_tool():
    """Get information about all drivers in the race."""
    return await get_all_drivers()


@mcp.tool()
async def get_team_info_tool(car_number: str):
    """Get team information for a specific car."""
    return await get_team_info(car_number)


# Telemetry Tools
@mcp.tool()
async def get_telemetry_channels_tool():
    """Get list of available telemetry channels."""
    return await get_telemetry_channels()


# Analysis Tools
@mcp.tool()
async def analyze_race_leader_tool():
    """Analyze who is currently leading the race and by how much."""
    return await analyze_race_leader()


@mcp.tool()
async def analyze_pit_strategy_tool(car_number: str):
    """Analyze pit stop strategy for a specific car."""
    return await analyze_pit_strategy(car_number)


@mcp.tool()
async def compare_lap_times_tool(car1: str, car2: str):
    """Compare lap times between two cars."""
    return await compare_lap_times(car1, car2)


def create_mcp_server() -> FastMCP:
    """Create and return the configured MCP server instance."""
    return mcp


async def main():
    """Run the MCP server."""
    print("=" * 60)
    print("TrackHouse MCP Server")
    print("=" * 60)
    print(f"\nConnecting to web server at: {WEB_SERVER_URL}")
    
    # Test connection
    health = await check_system_health()
    if "error" in health:
        print(f"\n⚠️  Web server not responding: {health['error']}")
        print("\nPlease ensure the edge server is running:")
        print("  cd edge_server")
        print("  docker-compose up")
    else:
        print(f"✓ System health: {health['status']}")
    
    print("\n" + "=" * 60)
    print("Available MCP Tools:")
    print("=" * 60)
    
    # List categories of tools
    tools = {
        "System": ["check_system_health", "get_vehicle_id"],
        "Car Data": ["get_car_position", "get_all_positions", "get_car_rank", 
                    "get_lap_time", "get_best_lap_time", "get_average_lap_time"],
        "Pit Stops": ["get_pit_events", "get_pit_times", "get_tire_data"],
        "Race Status": ["get_current_flag", "get_all_flags", "get_current_lap", 
                       "get_all_laps", "get_starting_grid", "get_track_info"],
        "Content": ["get_driver_info", "get_all_drivers", "get_team_info"],
        "Telemetry": ["get_telemetry_channels"],
        "Analysis": ["analyze_race_leader", "analyze_pit_strategy", "compare_lap_times"]
    }
    
    for category, tool_list in tools.items():
        print(f"\n{category}:")
        for tool in tool_list:
            print(f"  • {tool}")
    
    print("\n" + "=" * 60)
    print("MCP server is ready for connections!")
    print("=" * 60)
    
    # Run the MCP server
    await mcp.run()


if __name__ == "__main__":
    asyncio.run(main())