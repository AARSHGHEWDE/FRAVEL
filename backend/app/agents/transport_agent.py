from crewai import Agent, Task
from crewai.tools import BaseTool
import asyncio
from datetime import date

from app.config import settings
from app.tools.transport_tool import fetch_flights


class TransportSearchTool(BaseTool):
    name: str = "search_flights"
    description: str = "Search for flights between two cities on a given date"
    origin: str = ""
    destination: str = ""
    departure_date: date = date.today()
    travelers: int = 1

    def _run(self) -> str:
        flights = asyncio.run(fetch_flights(
            origin=self.origin, destination=self.destination,
            departure_date=self.departure_date, adults=self.travelers,
            api_key=settings.amadeus_api_key, api_secret=settings.amadeus_api_secret,
        ))
        if not flights:
            return "No flights found. Suggest alternative dates or nearby airports."
        return "\n".join(
            f"- {f.airline} {f.flight_number}: {f.origin}->{f.destination} "
            f"dep {f.departure_time} arr {f.arrival_time} ${f.price} {f.stops} stops ({f.cabin_class})"
            for f in flights
        )


def create_transport_agent(llm=None) -> Agent:
    return Agent(
        role="Transport Agent",
        goal="Find the best flight and train options for the trip",
        backstory="You are a travel logistics expert who finds the best transport options balancing price, duration, and convenience.",
        llm=llm, verbose=True,
    )


def create_transport_task(agent: Agent, origin: str, destination: str, departure_date: date, return_date: date, travelers: int) -> Task:
    tool = TransportSearchTool(origin=origin, destination=destination, departure_date=departure_date, travelers=travelers)
    return Task(
        description=f"Search for flights from {origin} to {destination} departing {departure_date} and returning {return_date} for {travelers} traveler(s). Return the top 5 options sorted by best value (price vs duration).",
        agent=agent, tools=[tool],
        expected_output="A list of top 5 flight options with prices, durations, and stops.",
    )
