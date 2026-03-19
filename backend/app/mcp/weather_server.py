from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

from app.config import settings
from app.tools.weather_tool import fetch_weather

server = Server("fravel-weather")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(
        name="get_weather_forecast",
        description="Get weather forecast for a city (5-day forecast)",
        inputSchema={"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
    )]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather_forecast":
        forecast = await fetch_weather(city=arguments["city"], api_key=settings.openweather_api_key)
        return [TextContent(type="text", text=forecast.model_dump_json())]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
