# import sys, asyncio
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# from weather_team.agents.weather_root_agent import build_weather_root
# root_agent = build_weather_root()

from weather_team.agents.mcp_obsidian_agent import build_obsidian_agent_async
root_agent = build_obsidian_agent_async()