import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import date

os.environ.setdefault("OLLAMA_MODEL", "test-model")
os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")

from app.agents.crew import build_crew
from app.models.trip import TripRequest


def make_mock_agent(role: str) -> MagicMock:
    agent = MagicMock()
    agent.role = role
    return agent


def make_mock_task() -> MagicMock:
    return MagicMock()


MOCK_AGENTS = [
    make_mock_agent("Transport Agent"),
    make_mock_agent("Events Agent"),
    make_mock_agent("Restaurant Agent"),
    make_mock_agent("Weather Agent"),
    make_mock_agent("Itinerary Compiler"),
]
MOCK_TASKS = [make_mock_task() for _ in range(5)]


@patch("app.agents.crew.get_llm", return_value=MagicMock())
@patch("app.agents.crew.create_itinerary_task", return_value=MOCK_TASKS[4])
@patch("app.agents.crew.create_weather_task", return_value=MOCK_TASKS[3])
@patch("app.agents.crew.create_restaurant_task", return_value=MOCK_TASKS[2])
@patch("app.agents.crew.create_events_task", return_value=MOCK_TASKS[1])
@patch("app.agents.crew.create_transport_task", return_value=MOCK_TASKS[0])
@patch("app.agents.crew.create_itinerary_agent", return_value=MOCK_AGENTS[4])
@patch("app.agents.crew.create_weather_agent", return_value=MOCK_AGENTS[3])
@patch("app.agents.crew.create_restaurant_agent", return_value=MOCK_AGENTS[2])
@patch("app.agents.crew.create_events_agent", return_value=MOCK_AGENTS[1])
@patch("app.agents.crew.create_transport_agent", return_value=MOCK_AGENTS[0])
@patch("app.agents.crew.Crew")
def test_build_crew_returns_crew_with_all_agents(
    mock_crew_cls,
    mock_transport_agent, mock_events_agent, mock_restaurant_agent,
    mock_weather_agent, mock_itinerary_agent,
    mock_transport_task, mock_events_task, mock_restaurant_task,
    mock_weather_task, mock_itinerary_task,
    mock_get_llm,
):
    mock_crew_instance = MagicMock()
    mock_crew_instance.agents = MOCK_AGENTS
    mock_crew_instance.tasks = MOCK_TASKS
    mock_crew_cls.return_value = mock_crew_instance

    trip = TripRequest(
        origin="New York", destination="Paris",
        departure_date=date(2026, 6, 15), return_date=date(2026, 6, 22),
        budget=3000.0, interests=["museums", "food"],
    )
    crew = build_crew(trip)
    assert crew is not None
    assert len(crew.agents) == 5
    assert len(crew.tasks) == 5


@patch("app.agents.crew.get_llm", return_value=MagicMock())
@patch("app.agents.crew.create_itinerary_task", return_value=MOCK_TASKS[4])
@patch("app.agents.crew.create_weather_task", return_value=MOCK_TASKS[3])
@patch("app.agents.crew.create_restaurant_task", return_value=MOCK_TASKS[2])
@patch("app.agents.crew.create_events_task", return_value=MOCK_TASKS[1])
@patch("app.agents.crew.create_transport_task", return_value=MOCK_TASKS[0])
@patch("app.agents.crew.create_itinerary_agent", return_value=MOCK_AGENTS[4])
@patch("app.agents.crew.create_weather_agent", return_value=MOCK_AGENTS[3])
@patch("app.agents.crew.create_restaurant_agent", return_value=MOCK_AGENTS[2])
@patch("app.agents.crew.create_events_agent", return_value=MOCK_AGENTS[1])
@patch("app.agents.crew.create_transport_agent", return_value=MOCK_AGENTS[0])
@patch("app.agents.crew.Crew")
def test_build_crew_agent_names(
    mock_crew_cls,
    mock_transport_agent, mock_events_agent, mock_restaurant_agent,
    mock_weather_agent, mock_itinerary_agent,
    mock_transport_task, mock_events_task, mock_restaurant_task,
    mock_weather_task, mock_itinerary_task,
    mock_get_llm,
):
    mock_crew_instance = MagicMock()
    mock_crew_instance.agents = MOCK_AGENTS
    mock_crew_instance.tasks = MOCK_TASKS
    mock_crew_cls.return_value = mock_crew_instance

    trip = TripRequest(
        origin="NYC", destination="Paris",
        departure_date=date(2026, 6, 15), return_date=date(2026, 6, 22),
    )
    crew = build_crew(trip)
    agent_roles = {a.role for a in crew.agents}
    assert agent_roles == {"Transport Agent", "Events Agent", "Restaurant Agent", "Weather Agent", "Itinerary Compiler"}
