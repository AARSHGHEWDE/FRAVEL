from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json

from app.config import settings
from app.tools.restaurant_tool import fetch_restaurants

server = Server("fravel-restaurants")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(
        name="search_restaurants",
        description="Search for top-rated restaurants in a city",
        inputSchema={
            "type": "object",
            "properties": {"location": {"type": "string"}, "cuisine": {"type": "string"}},
            "required": ["location"],
        },
    )]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_restaurants":
        restaurants = await fetch_restaurants(
            location=arguments["location"],
            api_key=settings.yelp_api_key,
            cuisine=arguments.get("cuisine"),
        )
        return [TextContent(type="text", text=json.dumps([r.model_dump(mode="json") for r in restaurants]))]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
