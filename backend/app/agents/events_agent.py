from crewai import Agent, Task
from crewai.tools import BaseTool
import asyncio
from datetime import date

from app.config import settings
from app.tools.events_tool import fetch_events


class EventSearchTool(BaseTool):
    name: str = "search_events"
    description: str = "Search for events in a city during given dates"
    city: str = ""
    start_date: date = date.today()
    end_date: date = date.today()

    def _run(self) -> str:
        events = asyncio.run(fetch_events(
            city=self.city, start_date=self.start_date, end_date=self.end_date,
            api_key=settings.ticketmaster_api_key,
        ))
        if not events:
            return "No events found during these dates."
        return "\n".join(
            f"- {e.name} at {e.venue} on {e.date} ({e.category}) {'$' + str(e.price) if e.price else 'Free'}"
            for e in events
        )


def create_events_agent(llm=None) -> Agent:
    return Agent(
        role="Events Agent",
        goal="Discover the best local events, festivals, and activities at the destination",
        backstory="You are a cultural events curator who finds the most exciting and relevant events happening at any destination.",
        llm=llm, verbose=True,
    )


def create_events_task(agent: Agent, city: str, start_date: date, end_date: date, interests: list[str]) -> Task:
    tool = EventSearchTool(city=city, start_date=start_date, end_date=end_date)
    interests_str = ", ".join(interests) if interests else "general sightseeing"
    return Task(
        description=f"Find events in {city} between {start_date} and {end_date}. The traveler is interested in: {interests_str}. Return the top 10 most relevant events.",
        agent=agent, tools=[tool],
        expected_output="A list of top 10 events with names, venues, dates, and prices.",
    )
