from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json
from datetime import date

from app.config import settings
from app.tools.transport_tool import fetch_flights

server = Server("fravel-transport")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(
        name="search_flights",
        description="Search for flights between two cities",
        inputSchema={
            "type": "object",
            "properties": {
                "origin": {"type": "string"}, "destination": {"type": "string"},
                "departure_date": {"type": "string"}, "adults": {"type": "integer", "default": 1},
            },
            "required": ["origin", "destination", "departure_date"],
        },
    )]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_flights":
        flights = await fetch_flights(
            origin=arguments["origin"], destination=arguments["destination"],
            departure_date=date.fromisoformat(arguments["departure_date"]),
            adults=arguments.get("adults", 1),
            api_key=settings.amadeus_api_key, api_secret=settings.amadeus_api_secret,
        )
        return [TextContent(type="text", text=json.dumps([f.model_dump(mode="json") for f in flights]))]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
