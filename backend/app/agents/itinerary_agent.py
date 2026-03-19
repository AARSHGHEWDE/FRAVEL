from crewai import Agent, Task


def create_itinerary_agent(llm=None) -> Agent:
    return Agent(
        role="Itinerary Compiler",
        goal="Compile all research into a coherent, time-optimized day-by-day itinerary",
        backstory="You are a master travel planner who creates perfectly timed itineraries balancing activities, meals, rest, and transit. You always consider weather, opening hours, and geography to minimize wasted time.",
        llm=llm, verbose=True,
    )


def create_itinerary_task(agent: Agent, destination: str, num_days: int, budget: float) -> Task:
    return Task(
        description=(
            f"Using all the research gathered by other agents, compile a {num_days}-day itinerary for {destination} with a ${budget} budget. "
            f"For each day, create a timeline with morning/afternoon/evening activities, restaurant recommendations, events, weather-appropriate suggestions, and estimated costs.\n"
            f'Output as structured JSON: {{"title": "...", "days": [{{"date": "YYYY-MM-DD", "title": "...", "activities": [{{"time": "HH:MM", "title": "...", "description": "...", "category": "sightseeing|food|transport|event|free", "cost": 0.0, "duration_minutes": 60, "location": "..."}}]}}], "total_cost": 0.0, "summary": "..."}}'
        ),
        agent=agent,
        expected_output="A complete JSON itinerary with day-by-day activities, costs, and summary.",
    )
