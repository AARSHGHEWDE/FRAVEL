from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json
from datetime import date

from app.config import settings
from app.tools.events_tool import fetch_events

server = Server("fravel-events")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(
        name="search_events",
        description="Search for events in a city during specific dates",
        inputSchema={
            "type": "object",
            "properties": {
                "city": {"type": "string"}, "start_date": {"type": "string"}, "end_date": {"type": "string"},
            },
            "required": ["city", "start_date", "end_date"],
        },
    )]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_events":
        events = await fetch_events(
            city=arguments["city"],
            start_date=date.fromisoformat(arguments["start_date"]),
            end_date=date.fromisoformat(arguments["end_date"]),
            api_key=settings.ticketmaster_api_key,
        )
        return [TextContent(type="text", text=json.dumps([e.model_dump(mode="json") for e in events], default=str))]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
