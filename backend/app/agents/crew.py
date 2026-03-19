from crewai import Crew, Process, LLM

from app.config import settings
from app.models.trip import TripRequest
from app.agents.transport_agent import create_transport_agent, create_transport_task
from app.agents.events_agent import create_events_agent, create_events_task
from app.agents.restaurant_agent import create_restaurant_agent, create_restaurant_task
from app.agents.weather_agent import create_weather_agent, create_weather_task
from app.agents.itinerary_agent import create_itinerary_agent, create_itinerary_task


def get_llm() -> LLM:
    return LLM(
        model=f"ollama/{settings.ollama_model}",
        base_url=settings.ollama_base_url,
    )


def build_crew(trip: TripRequest) -> Crew:
    num_days = (trip.return_date - trip.departure_date).days
    llm = get_llm()

    transport_agent = create_transport_agent(llm=llm)
    events_agent = create_events_agent(llm=llm)
    restaurant_agent = create_restaurant_agent(llm=llm)
    weather_agent = create_weather_agent(llm=llm)
    itinerary_agent = create_itinerary_agent(llm=llm)

    transport_task = create_transport_task(
        agent=transport_agent, origin=trip.origin, destination=trip.destination,
        departure_date=trip.departure_date, return_date=trip.return_date, travelers=trip.travelers,
    )
    events_task = create_events_task(
        agent=events_agent, city=trip.destination,
        start_date=trip.departure_date, end_date=trip.return_date, interests=trip.interests,
    )
    restaurant_task = create_restaurant_task(
        agent=restaurant_agent, city=trip.destination,
        interests=trip.interests, budget=trip.budget,
    )
    weather_task = create_weather_task(agent=weather_agent, city=trip.destination)
    itinerary_task = create_itinerary_task(
        agent=itinerary_agent, destination=trip.destination,
        num_days=num_days, budget=trip.budget,
    )

    return Crew(
        agents=[transport_agent, events_agent, restaurant_agent, weather_agent, itinerary_agent],
        tasks=[transport_task, events_task, restaurant_task, weather_task, itinerary_task],
        process=Process.sequential, verbose=True,
    )
