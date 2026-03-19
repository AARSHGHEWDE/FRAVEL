# FRAVEL - Agentic Travel & Event Planning Assistant Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-stack multi-agent travel planning app where CrewAI agents search flights, events, restaurants, and weather, then compile optimized itineraries — all streamed in real-time to a polished React UI.

**Architecture:** FastAPI backend orchestrates a CrewAI crew of 5 specialized agents (Transport, Events, Restaurant, Weather, Itinerary Compiler). Each agent uses custom tools that wrap external APIs. Real-time agent status streams to the React frontend via Server-Sent Events (SSE). Supabase handles auth and persistence. MCP servers expose each data source as a standalone protocol-compliant service.

**Tech Stack:** React 19 + Vite + TypeScript + Tailwind CSS 4 + Framer Motion (frontend), Python 3.12 + FastAPI + CrewAI + Pydantic (backend), Supabase (auth + DB), OpenWeather / Amadeus / Yelp Fusion / Ticketmaster APIs.

---

## File Structure

```
FRAVEL/
├── backend/
│   ├── pyproject.toml
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app, CORS, lifespan
│   │   ├── config.py                  # Pydantic Settings (env vars)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── trip.py                # TripRequest, TripResponse
│   │   │   ├── transport.py           # FlightOption, TrainOption
│   │   │   ├── event.py               # EventOption
│   │   │   ├── restaurant.py          # RestaurantOption
│   │   │   ├── weather.py             # WeatherForecast, DayWeather
│   │   │   └── itinerary.py           # Itinerary, DayPlan, Activity
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── transport_tool.py      # Amadeus API wrapper
│   │   │   ├── events_tool.py         # Ticketmaster API wrapper
│   │   │   ├── restaurant_tool.py     # Yelp Fusion API wrapper
│   │   │   └── weather_tool.py        # OpenWeather API wrapper
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── transport_agent.py     # CrewAI Agent + Task
│   │   │   ├── events_agent.py        # CrewAI Agent + Task
│   │   │   ├── restaurant_agent.py    # CrewAI Agent + Task
│   │   │   ├── weather_agent.py       # CrewAI Agent + Task
│   │   │   ├── itinerary_agent.py     # CrewAI Agent + Task
│   │   │   └── crew.py               # Crew assembly + kickoff
│   │   ├── mcp/
│   │   │   ├── __init__.py
│   │   │   ├── transport_server.py    # MCP server for transport
│   │   │   ├── events_server.py       # MCP server for events
│   │   │   ├── restaurant_server.py   # MCP server for restaurants
│   │   │   └── weather_server.py      # MCP server for weather
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── trips.py              # POST /trips, GET /trips, GET /trips/:id
│   │   │   ├── auth.py               # POST /auth/signup, /auth/login, /auth/me
│   │   │   └── sse.py                # GET /trips/:id/stream (SSE)
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── supabase_client.py     # Supabase client singleton
│   │       └── planner.py            # Orchestrates crew, emits SSE events
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py               # Fixtures: test client, mock APIs
│       ├── test_models.py
│       ├── test_tools/
│       │   ├── __init__.py
│       │   ├── test_transport_tool.py
│       │   ├── test_events_tool.py
│       │   ├── test_restaurant_tool.py
│       │   └── test_weather_tool.py
│       ├── test_agents/
│       │   ├── __init__.py
│       │   └── test_crew.py
│       └── test_routes/
│           ├── __init__.py
│           ├── test_trips.py
│           └── test_sse.py
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   ├── public/
│   │   └── favicon.svg
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css                  # Tailwind directives + custom fonts
│       ├── types/
│       │   └── index.ts              # All TypeScript interfaces
│       ├── lib/
│       │   ├── supabase.ts           # Supabase JS client
│       │   ├── api.ts                # Fetch wrapper for backend
│       │   └── sse.ts                # SSE connection helper
│       ├── store/
│       │   └── tripStore.ts          # Zustand store for trip state
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── useAgentStatus.ts
│       │   └── useTheme.ts
│       ├── components/
│       │   ├── ui/
│       │   │   ├── Button.tsx
│       │   │   ├── Input.tsx
│       │   │   ├── Card.tsx
│       │   │   ├── Badge.tsx
│       │   │   ├── DateRangePicker.tsx
│       │   │   ├── Select.tsx
│       │   │   ├── Slider.tsx
│       │   │   └── LoadingSpinner.tsx
│       │   ├── layout/
│       │   │   ├── Navbar.tsx
│       │   │   ├── Footer.tsx
│       │   │   └── ThemeToggle.tsx
│       │   ├── trip/
│       │   │   ├── TripForm.tsx
│       │   │   ├── TripCard.tsx
│       │   │   └── TripHistory.tsx
│       │   ├── itinerary/
│       │   │   ├── ItineraryView.tsx
│       │   │   ├── DayColumn.tsx
│       │   │   ├── ActivityCard.tsx
│       │   │   ├── FlightCard.tsx
│       │   │   ├── RestaurantCard.tsx
│       │   │   ├── EventCard.tsx
│       │   │   ├── WeatherBadge.tsx
│       │   │   └── ExportPDF.tsx
│       │   └── agents/
│       │       ├── AgentStatusPanel.tsx
│       │       └── AgentProgressRing.tsx
│       └── pages/
│           ├── Landing.tsx
│           ├── Plan.tsx
│           ├── Itinerary.tsx
│           ├── History.tsx
│           └── Auth.tsx
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
└── docs/
    └── superpowers/
        └── plans/
            └── 2026-03-18-fravel-travel-assistant.md
```

---

## Task 1: Backend Project Scaffolding

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.env.example`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/app/config.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`
- Create: `.gitignore`

- [ ] **Step 0: Create `.gitignore` (before any commits)**

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
.venv/
venv/

# Node
node_modules/
frontend/dist/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 1: Create `backend/pyproject.toml`**

```toml
[project]
name = "fravel-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "crewai>=0.108.0",
    "crewai-tools>=0.38.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
    "supabase>=2.12.0",
    "httpx>=0.28.0",
    "sse-starlette>=2.2.0",
    "python-dotenv>=1.0.0",
    "mcp>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.25.0",
    "pytest-httpx>=0.35.0",
    "respx>=0.22.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 2: Create `backend/.env.example`**

```env
# LLM (Ollama - no API key needed, just model name)
OLLAMA_MODEL=
OLLAMA_BASE_URL=http://localhost:11434

# External APIs
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
OPENWEATHER_API_KEY=your_openweather_key
YELP_API_KEY=your_yelp_key
TICKETMASTER_API_KEY=your_ticketmaster_key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# App
FRONTEND_URL=http://localhost:5173
```

- [ ] **Step 3: Create `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM (Ollama)
    ollama_model: str = ""  # e.g. "llama3", "mistral", "gemma2"
    ollama_base_url: str = "http://localhost:11434"

    # External APIs
    amadeus_api_key: str = ""
    amadeus_api_secret: str = ""
    openweather_api_key: str = ""
    yelp_api_key: str = ""
    ticketmaster_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""

    # App
    frontend_url: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
```

- [ ] **Step 4: Create `backend/app/main.py`**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(title="FRAVEL API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 5: Create `backend/app/__init__.py`** (empty file)

- [ ] **Step 6: Create `backend/tests/__init__.py`** (empty file)

- [ ] **Step 7: Create `backend/tests/conftest.py`**

```python
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
```

- [ ] **Step 8: Create virtual environment and install dependencies**

Run: `cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`
Expected: Successful installation

- [ ] **Step 9: Run health check test**

Run: `cd backend && python -c "from fastapi.testclient import TestClient; from app.main import app; c = TestClient(app); r = c.get('/health'); assert r.json() == {'status': 'ok'}; print('PASS')"`
Expected: `PASS`

- [ ] **Step 10: Commit**

```bash
git init
git add .gitignore backend/
git commit -m "feat: scaffold backend with FastAPI, CrewAI, and config"
```

---

## Task 2: Backend Data Models

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/trip.py`
- Create: `backend/app/models/transport.py`
- Create: `backend/app/models/event.py`
- Create: `backend/app/models/restaurant.py`
- Create: `backend/app/models/weather.py`
- Create: `backend/app/models/itinerary.py`
- Create: `backend/tests/test_models.py`

- [ ] **Step 1: Write failing tests for all models**

Create `backend/tests/test_models.py`:

```python
import pytest
from datetime import date, datetime


def test_trip_request_valid():
    from app.models.trip import TripRequest

    trip = TripRequest(
        origin="New York",
        destination="Paris",
        departure_date=date(2026, 6, 15),
        return_date=date(2026, 6, 22),
        budget=3000.0,
        interests=["museums", "food"],
        travelers=2,
    )
    assert trip.origin == "New York"
    assert trip.budget == 3000.0


def test_trip_request_return_after_departure():
    from app.models.trip import TripRequest

    with pytest.raises(ValueError):
        TripRequest(
            origin="NYC",
            destination="Paris",
            departure_date=date(2026, 6, 22),
            return_date=date(2026, 6, 15),
            budget=3000.0,
        )


def test_flight_option():
    from app.models.transport import FlightOption

    flight = FlightOption(
        airline="Delta",
        flight_number="DL123",
        origin="JFK",
        destination="CDG",
        departure_time=datetime(2026, 6, 15, 8, 0),
        arrival_time=datetime(2026, 6, 15, 20, 0),
        duration_minutes=720,
        price=850.0,
        currency="USD",
        stops=0,
        cabin_class="economy",
    )
    assert flight.airline == "Delta"
    assert flight.stops == 0


def test_event_option():
    from app.models.event import EventOption

    event = EventOption(
        name="Louvre Night Tour",
        venue="Louvre Museum",
        date=datetime(2026, 6, 16, 20, 0),
        category="museum",
        price=25.0,
        currency="USD",
        description="Evening tour of the Louvre",
        url="https://example.com",
        image_url="https://example.com/img.jpg",
    )
    assert event.name == "Louvre Night Tour"


def test_restaurant_option():
    from app.models.restaurant import RestaurantOption

    restaurant = RestaurantOption(
        name="Le Comptoir",
        cuisine="French",
        rating=4.5,
        price_level=3,
        address="123 Rue de Rivoli, Paris",
        phone="+33123456789",
        url="https://example.com",
        image_url="https://example.com/img.jpg",
        review_count=250,
    )
    assert restaurant.rating == 4.5
    assert restaurant.price_level == 3


def test_weather_forecast():
    from app.models.weather import DayWeather, WeatherForecast

    day = DayWeather(
        date=date(2026, 6, 15),
        temp_high_c=28.0,
        temp_low_c=18.0,
        condition="Sunny",
        icon="01d",
        humidity=45,
        wind_speed_kmh=12.0,
        precipitation_chance=10,
    )
    forecast = WeatherForecast(city="Paris", days=[day])
    assert forecast.city == "Paris"
    assert len(forecast.days) == 1


def test_itinerary():
    from app.models.itinerary import Activity, DayPlan, Itinerary

    activity = Activity(
        time="10:00",
        title="Visit Louvre",
        description="Explore the museum",
        category="sightseeing",
        cost=25.0,
        duration_minutes=180,
        location="Louvre Museum",
    )
    day = DayPlan(
        date=date(2026, 6, 16),
        title="Day 1 - Art & Culture",
        activities=[activity],
    )
    itinerary = Itinerary(
        trip_id="abc123",
        title="Paris Adventure",
        days=[day],
        total_cost=2500.0,
        currency="USD",
    )
    assert itinerary.title == "Paris Adventure"
    assert len(itinerary.days) == 1
    assert len(itinerary.days[0].activities) == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.models.trip'`

- [ ] **Step 3: Create all model files**

Create `backend/app/models/__init__.py`:
```python
from app.models.trip import TripRequest, TripResponse
from app.models.transport import FlightOption, TrainOption
from app.models.event import EventOption
from app.models.restaurant import RestaurantOption
from app.models.weather import DayWeather, WeatherForecast
from app.models.itinerary import Activity, DayPlan, Itinerary

__all__ = [
    "TripRequest", "TripResponse",
    "FlightOption", "TrainOption",
    "EventOption",
    "RestaurantOption",
    "DayWeather", "WeatherForecast",
    "Activity", "DayPlan", "Itinerary",
]
```

Create `backend/app/models/trip.py`:
```python
from datetime import date
from pydantic import BaseModel, model_validator


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: date
    budget: float = 5000.0
    interests: list[str] = []
    travelers: int = 1

    @model_validator(mode="after")
    def validate_dates(self):
        if self.return_date <= self.departure_date:
            raise ValueError("return_date must be after departure_date")
        return self


class TripResponse(BaseModel):
    trip_id: str
    status: str  # "pending", "planning", "complete", "error"
    request: TripRequest
    itinerary_id: str | None = None
```

Create `backend/app/models/transport.py`:
```python
from datetime import datetime
from pydantic import BaseModel


class FlightOption(BaseModel):
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    currency: str = "USD"
    stops: int = 0
    cabin_class: str = "economy"


class TrainOption(BaseModel):
    operator: str
    train_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    currency: str = "USD"
    class_type: str = "standard"
```

Create `backend/app/models/event.py`:
```python
from datetime import datetime
from pydantic import BaseModel


class EventOption(BaseModel):
    name: str
    venue: str
    date: datetime
    category: str
    price: float | None = None
    currency: str = "USD"
    description: str = ""
    url: str = ""
    image_url: str = ""
```

Create `backend/app/models/restaurant.py`:
```python
from pydantic import BaseModel, Field


class RestaurantOption(BaseModel):
    name: str
    cuisine: str
    rating: float = Field(ge=0, le=5)
    price_level: int = Field(ge=1, le=4)  # 1=cheap, 4=expensive
    address: str
    phone: str = ""
    url: str = ""
    image_url: str = ""
    review_count: int = 0
```

Create `backend/app/models/weather.py`:
```python
from datetime import date
from pydantic import BaseModel


class DayWeather(BaseModel):
    date: date
    temp_high_c: float
    temp_low_c: float
    condition: str  # "Sunny", "Cloudy", "Rain", etc.
    icon: str
    humidity: int
    wind_speed_kmh: float
    precipitation_chance: int  # 0-100


class WeatherForecast(BaseModel):
    city: str
    days: list[DayWeather]
```

Create `backend/app/models/itinerary.py`:
```python
from datetime import date
from pydantic import BaseModel

from app.models.weather import DayWeather


class Activity(BaseModel):
    time: str  # "10:00", "14:30"
    title: str
    description: str
    category: str  # "sightseeing", "food", "transport", "event", "free"
    cost: float = 0.0
    duration_minutes: int = 60
    location: str = ""
    latitude: float | None = None
    longitude: float | None = None


class DayPlan(BaseModel):
    date: date
    title: str
    activities: list[Activity]
    weather: DayWeather | None = None


class Itinerary(BaseModel):
    trip_id: str
    title: str
    days: list[DayPlan]
    total_cost: float
    currency: str = "USD"
    summary: str = ""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_models.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Create empty `__init__.py` files for tools and agents (needed before parallel tasks)**

Create `backend/app/tools/__init__.py` (empty).
Create `backend/app/agents/__init__.py` (empty).
Create `backend/app/services/__init__.py` (empty).
Create `backend/app/routes/__init__.py` (empty).
Create `backend/app/mcp/__init__.py` (empty).
Create `backend/tests/test_tools/__init__.py` (empty).
Create `backend/tests/test_agents/__init__.py` (empty).
Create `backend/tests/test_routes/__init__.py` (empty).

- [ ] **Step 6: Commit**

```bash
git add backend/app/models/ backend/app/tools/ backend/app/agents/ backend/app/services/ backend/app/routes/ backend/app/mcp/ backend/tests/
git commit -m "feat: add Pydantic data models for trips, transport, events, restaurants, weather, itineraries"
```

---

## Task 3: Backend Tools — Weather API

**Files:**
- Create: `backend/app/tools/__init__.py`
- Create: `backend/app/tools/weather_tool.py`
- Create: `backend/tests/test_tools/__init__.py`
- Create: `backend/tests/test_tools/test_weather_tool.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_tools/__init__.py` (empty).

Create `backend/tests/test_tools/test_weather_tool.py`:

```python
import pytest
import httpx
import respx
from datetime import date

from app.tools.weather_tool import fetch_weather


@respx.mock
@pytest.mark.asyncio
async def test_fetch_weather_returns_forecast():
    mock_response = {
        "city": {"name": "Paris"},
        "list": [
            {
                "dt": 1750003200,  # 2025-06-15 approx
                "main": {"temp_max": 28.0, "temp_min": 18.0, "humidity": 45},
                "weather": [{"main": "Clear", "icon": "01d"}],
                "wind": {"speed": 3.5},
                "pop": 0.1,
            }
        ],
    }
    respx.get("https://api.openweathermap.org/data/2.5/forecast").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await fetch_weather("Paris", api_key="test_key")
    assert result.city == "Paris"
    assert len(result.days) >= 1
    assert result.days[0].condition == "Clear"


@respx.mock
@pytest.mark.asyncio
async def test_fetch_weather_handles_api_error():
    respx.get("https://api.openweathermap.org/data/2.5/forecast").mock(
        return_value=httpx.Response(401, json={"message": "Invalid API key"})
    )

    result = await fetch_weather("Paris", api_key="bad_key")
    assert result.city == "Paris"
    assert len(result.days) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_tools/test_weather_tool.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement weather tool**

Create `backend/app/tools/weather_tool.py`:

```python
from datetime import date, datetime

import httpx

from app.models.weather import DayWeather, WeatherForecast

OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


async def fetch_weather(city: str, api_key: str) -> WeatherForecast:
    """Fetch 5-day weather forecast from OpenWeather API."""
    params = {"q": city, "appid": api_key, "units": "metric"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(OPENWEATHER_FORECAST_URL, params=params)

    if resp.status_code != 200:
        return WeatherForecast(city=city, days=[])

    data = resp.json()
    # OpenWeather returns 3-hour intervals; aggregate by day
    days_map: dict[date, list[dict]] = {}
    for entry in data.get("list", []):
        dt = datetime.fromtimestamp(entry["dt"])
        d = dt.date()
        days_map.setdefault(d, []).append(entry)

    days: list[DayWeather] = []
    for d, entries in sorted(days_map.items()):
        temps_high = [e["main"]["temp_max"] for e in entries]
        temps_low = [e["main"]["temp_min"] for e in entries]
        humidities = [e["main"]["humidity"] for e in entries]
        winds = [e["wind"]["speed"] for e in entries]
        pops = [e.get("pop", 0) for e in entries]

        # Use the most common weather condition
        conditions = [e["weather"][0]["main"] for e in entries]
        icons = [e["weather"][0]["icon"] for e in entries]

        days.append(
            DayWeather(
                date=d,
                temp_high_c=round(max(temps_high), 1),
                temp_low_c=round(min(temps_low), 1),
                condition=max(set(conditions), key=conditions.count),
                icon=max(set(icons), key=icons.count),
                humidity=round(sum(humidities) / len(humidities)),
                wind_speed_kmh=round(max(winds) * 3.6, 1),
                precipitation_chance=round(max(pops) * 100),
            )
        )

    return WeatherForecast(city=data.get("city", {}).get("name", city), days=days)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_tools/test_weather_tool.py -v`
Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/tools/ backend/tests/test_tools/
git commit -m "feat: add weather tool wrapping OpenWeather forecast API"
```

---

## Task 4: Backend Tools — Transport API (Amadeus)

**Files:**
- Create: `backend/app/tools/transport_tool.py`
- Create: `backend/tests/test_tools/test_transport_tool.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_tools/test_transport_tool.py`:

```python
import pytest
import httpx
import respx
from datetime import date

from app.tools.transport_tool import fetch_flights


@respx.mock
@pytest.mark.asyncio
async def test_fetch_flights_returns_options():
    # Mock Amadeus auth
    respx.post("https://api.amadeus.com/v1/security/oauth2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok123", "expires_in": 1799})
    )
    # Mock flight search
    respx.get("https://api.amadeus.com/v2/shopping/flight-offers").mock(
        return_value=httpx.Response(200, json={
            "data": [
                {
                    "itineraries": [
                        {
                            "duration": "PT12H0M",
                            "segments": [
                                {
                                    "carrierCode": "DL",
                                    "number": "123",
                                    "departure": {"iataCode": "JFK", "at": "2026-06-15T08:00:00"},
                                    "arrival": {"iataCode": "CDG", "at": "2026-06-15T20:00:00"},
                                }
                            ],
                        }
                    ],
                    "price": {"total": "850.00", "currency": "USD"},
                    "travelerPricings": [{"fareDetailsBySegment": [{"cabin": "ECONOMY"}]}],
                }
            ],
        })
    )

    flights = await fetch_flights(
        origin="JFK",
        destination="CDG",
        departure_date=date(2026, 6, 15),
        adults=1,
        api_key="key",
        api_secret="secret",
    )
    assert len(flights) == 1
    assert flights[0].airline == "DL"
    assert flights[0].price == 850.0


@respx.mock
@pytest.mark.asyncio
async def test_fetch_flights_handles_api_error():
    respx.post("https://api.amadeus.com/v1/security/oauth2/token").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )

    flights = await fetch_flights(
        origin="JFK",
        destination="CDG",
        departure_date=date(2026, 6, 15),
        adults=1,
        api_key="bad",
        api_secret="bad",
    )
    assert flights == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_tools/test_transport_tool.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement transport tool**

Create `backend/app/tools/transport_tool.py`:

```python
from datetime import date, datetime

import httpx

from app.models.transport import FlightOption

AMADEUS_AUTH_URL = "https://api.amadeus.com/v1/security/oauth2/token"
AMADEUS_FLIGHTS_URL = "https://api.amadeus.com/v2/shopping/flight-offers"


async def _get_amadeus_token(api_key: str, api_secret: str) -> str | None:
    """Get OAuth2 token from Amadeus."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            AMADEUS_AUTH_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": api_key,
                "client_secret": api_secret,
            },
        )
    if resp.status_code != 200:
        return None
    return resp.json().get("access_token")


def _parse_duration(iso_duration: str) -> int:
    """Parse ISO 8601 duration like 'PT12H30M' to minutes."""
    import re
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", iso_duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    return hours * 60 + minutes


async def fetch_flights(
    origin: str,
    destination: str,
    departure_date: date,
    adults: int,
    api_key: str,
    api_secret: str,
    max_results: int = 10,
) -> list[FlightOption]:
    """Fetch flight offers from Amadeus API."""
    token = await _get_amadeus_token(api_key, api_secret)
    if not token:
        return []

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date.isoformat(),
        "adults": adults,
        "max": max_results,
        "currencyCode": "USD",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            AMADEUS_FLIGHTS_URL,
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )

    if resp.status_code != 200:
        return []

    flights: list[FlightOption] = []
    for offer in resp.json().get("data", []):
        itinerary = offer["itineraries"][0]
        segments = itinerary["segments"]
        first_seg = segments[0]
        last_seg = segments[-1]
        cabin = offer["travelerPricings"][0]["fareDetailsBySegment"][0].get("cabin", "ECONOMY")

        flights.append(
            FlightOption(
                airline=first_seg["carrierCode"],
                flight_number=f"{first_seg['carrierCode']}{first_seg['number']}",
                origin=first_seg["departure"]["iataCode"],
                destination=last_seg["arrival"]["iataCode"],
                departure_time=datetime.fromisoformat(first_seg["departure"]["at"]),
                arrival_time=datetime.fromisoformat(last_seg["arrival"]["at"]),
                duration_minutes=_parse_duration(itinerary["duration"]),
                price=float(offer["price"]["total"]),
                currency=offer["price"].get("currency", "USD"),
                stops=len(segments) - 1,
                cabin_class=cabin.lower(),
            )
        )

    return flights
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_tools/test_transport_tool.py -v`
Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/tools/transport_tool.py backend/tests/test_tools/test_transport_tool.py
git commit -m "feat: add transport tool wrapping Amadeus flight search API"
```

---

## Task 5: Backend Tools — Events API (Ticketmaster)

**Files:**
- Create: `backend/app/tools/events_tool.py`
- Create: `backend/tests/test_tools/test_events_tool.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_tools/test_events_tool.py`:

```python
import pytest
import httpx
import respx
from datetime import date

from app.tools.events_tool import fetch_events


@respx.mock
@pytest.mark.asyncio
async def test_fetch_events_returns_options():
    respx.get("https://app.ticketmaster.com/discovery/v2/events.json").mock(
        return_value=httpx.Response(200, json={
            "_embedded": {
                "events": [
                    {
                        "name": "Jazz Festival",
                        "_embedded": {"venues": [{"name": "Olympia Hall"}]},
                        "dates": {"start": {"dateTime": "2026-06-16T20:00:00Z"}},
                        "classifications": [{"segment": {"name": "Music"}}],
                        "priceRanges": [{"min": 50.0, "currency": "USD"}],
                        "info": "A night of jazz",
                        "url": "https://example.com/event",
                        "images": [{"url": "https://example.com/img.jpg"}],
                    }
                ]
            }
        })
    )

    events = await fetch_events(
        city="Paris",
        start_date=date(2026, 6, 15),
        end_date=date(2026, 6, 22),
        api_key="test_key",
    )
    assert len(events) == 1
    assert events[0].name == "Jazz Festival"
    assert events[0].venue == "Olympia Hall"


@respx.mock
@pytest.mark.asyncio
async def test_fetch_events_handles_no_results():
    respx.get("https://app.ticketmaster.com/discovery/v2/events.json").mock(
        return_value=httpx.Response(200, json={})
    )

    events = await fetch_events(
        city="Nowhere",
        start_date=date(2026, 6, 15),
        end_date=date(2026, 6, 22),
        api_key="test_key",
    )
    assert events == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_tools/test_events_tool.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement events tool**

Create `backend/app/tools/events_tool.py`:

```python
from datetime import date, datetime

import httpx

from app.models.event import EventOption

TICKETMASTER_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


async def fetch_events(
    city: str,
    start_date: date,
    end_date: date,
    api_key: str,
    max_results: int = 20,
) -> list[EventOption]:
    """Fetch events from Ticketmaster Discovery API."""
    params = {
        "apikey": api_key,
        "city": city,
        "startDateTime": f"{start_date.isoformat()}T00:00:00Z",
        "endDateTime": f"{end_date.isoformat()}T23:59:59Z",
        "size": max_results,
        "sort": "relevance,desc",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(TICKETMASTER_URL, params=params)

    if resp.status_code != 200:
        return []

    data = resp.json()
    raw_events = data.get("_embedded", {}).get("events", [])

    events: list[EventOption] = []
    for raw in raw_events:
        venues = raw.get("_embedded", {}).get("venues", [{}])
        venue_name = venues[0].get("name", "Unknown") if venues else "Unknown"

        date_str = raw.get("dates", {}).get("start", {}).get("dateTime", "")
        event_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")) if date_str else datetime.now()

        classifications = raw.get("classifications", [{}])
        category = classifications[0].get("segment", {}).get("name", "Other") if classifications else "Other"

        price_ranges = raw.get("priceRanges", [])
        price = price_ranges[0].get("min") if price_ranges else None
        currency = price_ranges[0].get("currency", "USD") if price_ranges else "USD"

        images = raw.get("images", [])
        image_url = images[0].get("url", "") if images else ""

        events.append(
            EventOption(
                name=raw.get("name", ""),
                venue=venue_name,
                date=event_date,
                category=category,
                price=price,
                currency=currency,
                description=raw.get("info", ""),
                url=raw.get("url", ""),
                image_url=image_url,
            )
        )

    return events
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_tools/test_events_tool.py -v`
Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/tools/events_tool.py backend/tests/test_tools/test_events_tool.py
git commit -m "feat: add events tool wrapping Ticketmaster Discovery API"
```

---

## Task 6: Backend Tools — Restaurant API (Yelp)

**Files:**
- Create: `backend/app/tools/restaurant_tool.py`
- Create: `backend/tests/test_tools/test_restaurant_tool.py`

- [ ] **Step 1: Write failing test**

Create `backend/tests/test_tools/test_restaurant_tool.py`:

```python
import pytest
import httpx
import respx

from app.tools.restaurant_tool import fetch_restaurants


@respx.mock
@pytest.mark.asyncio
async def test_fetch_restaurants_returns_options():
    respx.get("https://api.yelp.com/v3/businesses/search").mock(
        return_value=httpx.Response(200, json={
            "businesses": [
                {
                    "name": "Le Comptoir",
                    "categories": [{"title": "French"}],
                    "rating": 4.5,
                    "price": "$$$",
                    "location": {"display_address": ["123 Rue de Rivoli", "Paris"]},
                    "phone": "+33123456789",
                    "url": "https://yelp.com/biz/123",
                    "image_url": "https://example.com/img.jpg",
                    "review_count": 250,
                }
            ]
        })
    )

    restaurants = await fetch_restaurants(
        location="Paris",
        api_key="test_key",
    )
    assert len(restaurants) == 1
    assert restaurants[0].name == "Le Comptoir"
    assert restaurants[0].cuisine == "French"
    assert restaurants[0].price_level == 3


@respx.mock
@pytest.mark.asyncio
async def test_fetch_restaurants_handles_api_error():
    respx.get("https://api.yelp.com/v3/businesses/search").mock(
        return_value=httpx.Response(500, json={"error": {"code": "INTERNAL_ERROR"}})
    )

    restaurants = await fetch_restaurants(location="Paris", api_key="bad_key")
    assert restaurants == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_tools/test_restaurant_tool.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement restaurant tool**

Create `backend/app/tools/restaurant_tool.py`:

```python
import httpx

from app.models.restaurant import RestaurantOption

YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"


def _price_to_level(price_str: str) -> int:
    """Convert Yelp price string ('$', '$$', '$$$', '$$$$') to int."""
    return len(price_str) if price_str else 2


async def fetch_restaurants(
    location: str,
    api_key: str,
    cuisine: str | None = None,
    max_results: int = 20,
) -> list[RestaurantOption]:
    """Fetch top restaurants from Yelp Fusion API."""
    params: dict = {
        "location": location,
        "term": f"{cuisine} restaurants" if cuisine else "restaurants",
        "sort_by": "rating",
        "limit": max_results,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(YELP_SEARCH_URL, params=params, headers=headers)

    if resp.status_code != 200:
        return []

    restaurants: list[RestaurantOption] = []
    for biz in resp.json().get("businesses", []):
        categories = biz.get("categories", [])
        cuisine_name = categories[0].get("title", "Unknown") if categories else "Unknown"
        address_parts = biz.get("location", {}).get("display_address", [])

        restaurants.append(
            RestaurantOption(
                name=biz.get("name", ""),
                cuisine=cuisine_name,
                rating=biz.get("rating", 0),
                price_level=_price_to_level(biz.get("price", "$$")),
                address=", ".join(address_parts),
                phone=biz.get("phone", ""),
                url=biz.get("url", ""),
                image_url=biz.get("image_url", ""),
                review_count=biz.get("review_count", 0),
            )
        )

    return restaurants
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_tools/test_restaurant_tool.py -v`
Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/tools/restaurant_tool.py backend/tests/test_tools/test_restaurant_tool.py
git commit -m "feat: add restaurant tool wrapping Yelp Fusion API"
```

---

## Task 7: Backend Agents — CrewAI Setup

**Files:**
- Create: `backend/app/agents/__init__.py`
- Create: `backend/app/agents/transport_agent.py`
- Create: `backend/app/agents/events_agent.py`
- Create: `backend/app/agents/restaurant_agent.py`
- Create: `backend/app/agents/weather_agent.py`
- Create: `backend/app/agents/itinerary_agent.py`
- Create: `backend/app/agents/crew.py`
- Create: `backend/tests/test_agents/__init__.py`
- Create: `backend/tests/test_agents/test_crew.py`

- [ ] **Step 1: Write failing test for crew assembly**

Create `backend/tests/test_agents/__init__.py` (empty).

Create `backend/tests/test_agents/test_crew.py`:

```python
import os
import pytest
from unittest.mock import patch
from datetime import date

# Set Ollama config for tests (no API key needed, just model name)
os.environ.setdefault("OLLAMA_MODEL", "test-model")
os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")

from app.agents.crew import build_crew
from app.models.trip import TripRequest


@patch("crewai.Agent.__init__", return_value=None)
def test_build_crew_returns_crew_with_all_agents(mock_agent_init):
    # Mock Agent.__init__ to avoid LLM validation
    mock_agent_init.side_effect = lambda self, **kwargs: self.__dict__.update(kwargs)
    trip = TripRequest(
        origin="New York",
        destination="Paris",
        departure_date=date(2026, 6, 15),
        return_date=date(2026, 6, 22),
        budget=3000.0,
        interests=["museums", "food"],
    )
    crew = build_crew(trip)
    assert crew is not None
    assert len(crew.agents) == 5
    assert len(crew.tasks) == 5


@patch("crewai.Agent.__init__", return_value=None)
def test_build_crew_agent_names(mock_agent_init):
    mock_agent_init.side_effect = lambda self, **kwargs: self.__dict__.update(kwargs)
    trip = TripRequest(
        origin="NYC",
        destination="Paris",
        departure_date=date(2026, 6, 15),
        return_date=date(2026, 6, 22),
    )
    crew = build_crew(trip)
    agent_roles = {a.role for a in crew.agents}
    expected_roles = {
        "Transport Agent",
        "Events Agent",
        "Restaurant Agent",
        "Weather Agent",
        "Itinerary Compiler",
    }
    assert agent_roles == expected_roles
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_agents/test_crew.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement all agents and crew**

Create `backend/app/agents/transport_agent.py`:

```python
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
        flights = asyncio.run(
            fetch_flights(
                origin=self.origin,
                destination=self.destination,
                departure_date=self.departure_date,
                adults=self.travelers,
                api_key=settings.amadeus_api_key,
                api_secret=settings.amadeus_api_secret,
            )
        )
        if not flights:
            return "No flights found. Suggest alternative dates or nearby airports."
        return "\n".join(
            f"- {f.airline} {f.flight_number}: {f.origin}->{f.destination} "
            f"dep {f.departure_time} arr {f.arrival_time} "
            f"${f.price} {f.stops} stops ({f.cabin_class})"
            for f in flights
        )


def create_transport_agent(llm=None) -> Agent:
    return Agent(
        role="Transport Agent",
        goal="Find the best flight and train options for the trip",
        backstory=(
            "You are a travel logistics expert who finds the best transport "
            "options balancing price, duration, and convenience."
        ),
        llm=llm,
        verbose=True,
    )


def create_transport_task(
    agent: Agent,
    origin: str,
    destination: str,
    departure_date: date,
    return_date: date,
    travelers: int,
) -> Task:
    tool = TransportSearchTool(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        travelers=travelers,
    )
    return Task(
        description=(
            f"Search for flights from {origin} to {destination} "
            f"departing {departure_date} and returning {return_date} "
            f"for {travelers} traveler(s). Return the top 5 options "
            f"sorted by best value (price vs duration)."
        ),
        agent=agent,
        tools=[tool],
        expected_output="A list of top 5 flight options with prices, durations, and stops.",
    )
```

Create `backend/app/agents/events_agent.py`:

```python
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
        events = asyncio.run(
            fetch_events(
                city=self.city,
                start_date=self.start_date,
                end_date=self.end_date,
                api_key=settings.ticketmaster_api_key,
            )
        )
        if not events:
            return "No events found during these dates."
        return "\n".join(
            f"- {e.name} at {e.venue} on {e.date} ({e.category}) "
            f"{'$' + str(e.price) if e.price else 'Free'}"
            for e in events
        )


def create_events_agent(llm=None) -> Agent:
    return Agent(
        role="Events Agent",
        goal="Discover the best local events, festivals, and activities at the destination",
        backstory=(
            "You are a cultural events curator who finds the most exciting "
            "and relevant events happening at any destination."
        ),
        llm=llm,
        verbose=True,
    )


def create_events_task(
    agent: Agent, city: str, start_date: date, end_date: date, interests: list[str]
) -> Task:
    tool = EventSearchTool(city=city, start_date=start_date, end_date=end_date)
    interests_str = ", ".join(interests) if interests else "general sightseeing"
    return Task(
        description=(
            f"Find events in {city} between {start_date} and {end_date}. "
            f"The traveler is interested in: {interests_str}. "
            f"Return the top 10 most relevant events."
        ),
        agent=agent,
        tools=[tool],
        expected_output="A list of top 10 events with names, venues, dates, and prices.",
    )
```

Create `backend/app/agents/restaurant_agent.py`:

```python
from crewai import Agent, Task
from crewai.tools import BaseTool
import asyncio

from app.config import settings
from app.tools.restaurant_tool import fetch_restaurants


class RestaurantSearchTool(BaseTool):
    name: str = "search_restaurants"
    description: str = "Search for top restaurants in a city"

    location: str = ""

    def _run(self) -> str:
        restaurants = asyncio.run(
            fetch_restaurants(
                location=self.location,
                api_key=settings.yelp_api_key,
            )
        )
        if not restaurants:
            return "No restaurants found."
        return "\n".join(
            f"- {r.name} ({r.cuisine}) - {r.rating}/5 "
            f"{'$' * r.price_level} - {r.review_count} reviews"
            for r in restaurants
        )


def create_restaurant_agent(llm=None) -> Agent:
    return Agent(
        role="Restaurant Agent",
        goal="Find the best restaurants at the destination matching traveler preferences",
        backstory=(
            "You are a food critic and restaurant guide who knows the best "
            "dining options in every city, from street food to fine dining."
        ),
        llm=llm,
        verbose=True,
    )


def create_restaurant_task(
    agent: Agent, city: str, interests: list[str], budget: float
) -> Task:
    tool = RestaurantSearchTool(location=city)
    food_interests = [i for i in interests if i in ["food", "fine dining", "street food", "local cuisine"]]
    cuisine_hint = f" focusing on {', '.join(food_interests)}" if food_interests else ""
    return Task(
        description=(
            f"Find the top 10 restaurants in {city}{cuisine_hint}. "
            f"Budget is approximately ${budget} total for the trip. "
            f"Include a mix of price ranges."
        ),
        agent=agent,
        tools=[tool],
        expected_output="A list of top 10 restaurants with names, cuisines, ratings, and price levels.",
    )
```

Create `backend/app/agents/weather_agent.py`:

```python
from crewai import Agent, Task
from crewai.tools import BaseTool
import asyncio

from app.config import settings
from app.tools.weather_tool import fetch_weather


class WeatherForecastTool(BaseTool):
    name: str = "get_weather"
    description: str = "Get weather forecast for a city"

    city: str = ""

    def _run(self) -> str:
        forecast = asyncio.run(
            fetch_weather(city=self.city, api_key=settings.openweather_api_key)
        )
        if not forecast.days:
            return "Weather data unavailable."
        return "\n".join(
            f"- {d.date}: {d.condition}, {d.temp_low_c}-{d.temp_high_c}°C, "
            f"rain {d.precipitation_chance}%, wind {d.wind_speed_kmh} km/h"
            for d in forecast.days
        )


def create_weather_agent(llm=None) -> Agent:
    return Agent(
        role="Weather Agent",
        goal="Provide accurate weather forecasts for trip planning",
        backstory=(
            "You are a meteorologist who provides clear, actionable weather "
            "forecasts to help travelers pack and plan activities."
        ),
        llm=llm,
        verbose=True,
    )


def create_weather_task(agent: Agent, city: str) -> Task:
    tool = WeatherForecastTool(city=city)
    return Task(
        description=(
            f"Get the weather forecast for {city}. "
            f"Summarize conditions and recommend clothing/gear."
        ),
        agent=agent,
        tools=[tool],
        expected_output="Day-by-day weather summary with packing recommendations.",
    )
```

Create `backend/app/agents/itinerary_agent.py`:

```python
from crewai import Agent, Task


def create_itinerary_agent(llm=None) -> Agent:
    return Agent(
        role="Itinerary Compiler",
        goal="Compile all research into a coherent, time-optimized day-by-day itinerary",
        backstory=(
            "You are a master travel planner who creates perfectly timed "
            "itineraries balancing activities, meals, rest, and transit. "
            "You always consider weather, opening hours, and geography "
            "to minimize wasted time."
        ),
        llm=llm,
        verbose=True,
    )


def create_itinerary_task(agent: Agent, destination: str, num_days: int, budget: float) -> Task:
    return Task(
        description=(
            f"Using all the research gathered by other agents, compile a "
            f"{num_days}-day itinerary for {destination} with a ${budget} budget. "
            f"For each day, create a timeline with:\n"
            f"- Morning, afternoon, and evening activities\n"
            f"- Restaurant recommendations for lunch and dinner\n"
            f"- Events that fall on that specific date\n"
            f"- Weather-appropriate suggestions\n"
            f"- Estimated costs per activity\n"
            f"Output as structured JSON matching this format:\n"
            f'{{"title": "...", "days": [{{"date": "YYYY-MM-DD", "title": "...", '
            f'"activities": [{{"time": "HH:MM", "title": "...", "description": "...", '
            f'"category": "sightseeing|food|transport|event|free", "cost": 0.0, '
            f'"duration_minutes": 60, "location": "..."}}]}}], '
            f'"total_cost": 0.0, "summary": "..."}}'
        ),
        agent=agent,
        expected_output="A complete JSON itinerary with day-by-day activities, costs, and summary.",
    )
```

Create `backend/app/agents/crew.py`:

```python
from crewai import Crew, Process, LLM

from app.config import settings
from app.models.trip import TripRequest
from app.agents.transport_agent import create_transport_agent, create_transport_task
from app.agents.events_agent import create_events_agent, create_events_task
from app.agents.restaurant_agent import create_restaurant_agent, create_restaurant_task
from app.agents.weather_agent import create_weather_agent, create_weather_task
from app.agents.itinerary_agent import create_itinerary_agent, create_itinerary_task


def get_llm() -> LLM:
    """Create Ollama LLM instance for CrewAI agents."""
    return LLM(
        model=f"ollama/{settings.ollama_model}",
        base_url=settings.ollama_base_url,
    )


def build_crew(trip: TripRequest) -> Crew:
    """Build a CrewAI crew for trip planning."""
    num_days = (trip.return_date - trip.departure_date).days

    # Create agents with Ollama LLM
    llm = get_llm()
    transport_agent = create_transport_agent(llm=llm)
    events_agent = create_events_agent(llm=llm)
    restaurant_agent = create_restaurant_agent(llm=llm)
    weather_agent = create_weather_agent(llm=llm)
    itinerary_agent = create_itinerary_agent(llm=llm)

    # Create tasks
    transport_task = create_transport_task(
        agent=transport_agent,
        origin=trip.origin,
        destination=trip.destination,
        departure_date=trip.departure_date,
        return_date=trip.return_date,
        travelers=trip.travelers,
    )
    events_task = create_events_task(
        agent=events_agent,
        city=trip.destination,
        start_date=trip.departure_date,
        end_date=trip.return_date,
        interests=trip.interests,
    )
    restaurant_task = create_restaurant_task(
        agent=restaurant_agent,
        city=trip.destination,
        interests=trip.interests,
        budget=trip.budget,
    )
    weather_task = create_weather_task(
        agent=weather_agent,
        city=trip.destination,
    )
    itinerary_task = create_itinerary_task(
        agent=itinerary_agent,
        destination=trip.destination,
        num_days=num_days,
        budget=trip.budget,
    )

    return Crew(
        agents=[transport_agent, events_agent, restaurant_agent, weather_agent, itinerary_agent],
        tasks=[transport_task, events_task, restaurant_task, weather_task, itinerary_task],
        process=Process.sequential,
        verbose=True,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_agents/test_crew.py -v`
Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/ backend/tests/test_agents/
git commit -m "feat: add CrewAI agents for transport, events, restaurants, weather, and itinerary compilation"
```

---

## Task 8: Backend Services — Supabase Client & Planner

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/supabase_client.py`
- Create: `backend/app/services/planner.py`

- [ ] **Step 1: Create `backend/app/services/__init__.py`** (empty)

- [ ] **Step 2: Create Supabase client**

Create `backend/app/services/supabase_client.py`:

```python
from supabase import create_client, Client

from app.config import settings

_client: Client | None = None


def get_supabase() -> Client:
    """Get or create Supabase client singleton."""
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_service_key)
    return _client
```

- [ ] **Step 3: Create planner service**

Create `backend/app/services/planner.py`:

```python
import asyncio
import json
import uuid
from collections.abc import AsyncGenerator

from app.models.trip import TripRequest
from app.models.itinerary import Itinerary
from app.agents.crew import build_crew
from app.services.supabase_client import get_supabase


class PlannerService:
    """Orchestrates the CrewAI crew and streams status via SSE."""

    def __init__(self, trip_request: TripRequest, trip_id: str | None = None):
        self.trip = trip_request
        self.trip_id = trip_id or str(uuid.uuid4())
        self._status_queue: asyncio.Queue[dict] = asyncio.Queue()

    async def _emit(self, agent: str, status: str, detail: str = ""):
        await self._status_queue.put({
            "agent": agent,
            "status": status,
            "detail": detail,
        })

    async def stream_status(self) -> AsyncGenerator[dict, None]:
        """Yield SSE events as the crew works."""
        while True:
            event = await self._status_queue.get()
            yield event
            if event.get("status") == "complete" and event.get("agent") == "system":
                break

    async def plan(self) -> str:
        """Run the crew and return the itinerary JSON."""
        crew = build_crew(self.trip)

        await self._emit("system", "started", "Planning your trip...")

        agent_names = [
            "Transport Agent",
            "Events Agent",
            "Restaurant Agent",
            "Weather Agent",
            "Itinerary Compiler",
        ]
        for name in agent_names:
            await self._emit(name, "working", f"{name} is researching...")

        # Run crew in a thread to not block the event loop
        result = await asyncio.to_thread(crew.kickoff)

        for name in agent_names:
            await self._emit(name, "done")

        # Save to Supabase
        try:
            db = get_supabase()
            db.table("trips").upsert({
                "id": self.trip_id,
                "request": self.trip.model_dump(mode="json"),
                "result": str(result),
                "status": "complete",
            }).execute()
        except Exception:
            pass  # Don't fail if DB is unavailable

        await self._emit("system", "complete", str(result))
        return str(result)
```

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/
git commit -m "feat: add Supabase client and planner orchestration service with SSE streaming"
```

---

## Task 9: Backend Routes — Trips, Auth, SSE

**Files:**
- Create: `backend/app/routes/__init__.py`
- Create: `backend/app/routes/trips.py`
- Create: `backend/app/routes/auth.py`
- Create: `backend/app/routes/sse.py`
- Modify: `backend/app/main.py` (add routers)
- Create: `backend/tests/test_routes/__init__.py`
- Create: `backend/tests/test_routes/test_trips.py`

- [ ] **Step 1: Write failing test for trip creation**

Create `backend/tests/test_routes/__init__.py` (empty).

Create `backend/tests/test_routes/test_trips.py`:

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_trip_returns_trip_id(client):
    response = client.post("/api/trips", json={
        "origin": "New York",
        "destination": "Paris",
        "departure_date": "2026-06-15",
        "return_date": "2026-06-22",
        "budget": 3000.0,
        "interests": ["museums"],
        "travelers": 2,
    })
    assert response.status_code == 201
    data = response.json()
    assert "trip_id" in data
    assert data["status"] == "pending"


def test_create_trip_invalid_dates(client):
    response = client.post("/api/trips", json={
        "origin": "NYC",
        "destination": "Paris",
        "departure_date": "2026-06-22",
        "return_date": "2026-06-15",
    })
    assert response.status_code == 422
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && pytest tests/test_routes/test_trips.py -v`
Expected: FAIL — 404 because routes not registered

- [ ] **Step 3: Implement routes**

Create `backend/app/routes/__init__.py` (empty).

Create `backend/app/routes/trips.py`:

```python
import asyncio
import uuid

from fastapi import APIRouter, BackgroundTasks

from app.models.trip import TripRequest, TripResponse
from app.services.planner import PlannerService

router = APIRouter(prefix="/api/trips", tags=["trips"])

# In-memory store for demo; production uses Supabase
_trips: dict[str, dict] = {}
_planners: dict[str, PlannerService] = {}


@router.post("", status_code=201)
async def create_trip(
    trip: TripRequest,
    background_tasks: BackgroundTasks,
) -> TripResponse:
    trip_id = str(uuid.uuid4())
    planner = PlannerService(trip, trip_id)
    _trips[trip_id] = {"request": trip, "status": "pending"}
    _planners[trip_id] = planner

    # Start planning in background
    background_tasks.add_task(planner.plan)

    return TripResponse(
        trip_id=trip_id,
        status="pending",
        request=trip,
    )


@router.get("/{trip_id}")
async def get_trip(trip_id: str) -> TripResponse:
    trip_data = _trips.get(trip_id)
    if not trip_data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripResponse(
        trip_id=trip_id,
        status=trip_data["status"],
        request=trip_data["request"],
    )


def get_planner(trip_id: str) -> PlannerService | None:
    return _planners.get(trip_id)
```

Create `backend/app/routes/auth.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.supabase_client import get_supabase

router = APIRouter(prefix="/api/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    user_id: str


@router.post("/signup")
async def signup(req: AuthRequest) -> AuthResponse:
    try:
        db = get_supabase()
        result = db.auth.sign_up({"email": req.email, "password": req.password})
        return AuthResponse(
            access_token=result.session.access_token,
            user_id=result.user.id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(req: AuthRequest) -> AuthResponse:
    try:
        db = get_supabase()
        result = db.auth.sign_in_with_password({"email": req.email, "password": req.password})
        return AuthResponse(
            access_token=result.session.access_token,
            user_id=result.user.id,
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
```

Create `backend/app/routes/sse.py`:

```python
import asyncio
import json

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.routes.trips import get_planner

router = APIRouter(prefix="/api/trips", tags=["sse"])


@router.get("/{trip_id}/stream")
async def stream_trip_status(trip_id: str):
    planner = get_planner(trip_id)
    if not planner:
        raise HTTPException(status_code=404, detail="Trip not found")

    async def event_generator():
        async for event in planner.stream_status():
            yield {"event": "agent_status", "data": json.dumps(event)}

    return EventSourceResponse(event_generator())
```

- [ ] **Step 4: Register routers in main.py**

Update `backend/app/main.py` to add at the bottom (before the health check):

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import trips, auth, sse


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="FRAVEL API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router)
app.include_router(auth.router)
app.include_router(sse.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd backend && pytest tests/test_routes/test_trips.py -v`
Expected: All 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add backend/app/routes/ backend/app/main.py backend/tests/test_routes/
git commit -m "feat: add API routes for trips, auth, and SSE streaming"
```

---

## Task 10: Backend MCP Servers

**Files:**
- Create: `backend/app/mcp/__init__.py`
- Create: `backend/app/mcp/transport_server.py`
- Create: `backend/app/mcp/events_server.py`
- Create: `backend/app/mcp/restaurant_server.py`
- Create: `backend/app/mcp/weather_server.py`

- [ ] **Step 1: Create MCP server for weather**

Create `backend/app/mcp/__init__.py` (empty).

Create `backend/app/mcp/weather_server.py`:

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json

from app.config import settings
from app.tools.weather_tool import fetch_weather

server = Server("fravel-weather")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather_forecast",
            description="Get weather forecast for a city (5-day forecast)",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather_forecast":
        forecast = await fetch_weather(
            city=arguments["city"],
            api_key=settings.openweather_api_key,
        )
        return [TextContent(type="text", text=forecast.model_dump_json())]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 2: Create MCP server for transport**

Create `backend/app/mcp/transport_server.py`:

```python
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
    return [
        Tool(
            name="search_flights",
            description="Search for flights between two cities",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Origin airport code (e.g. JFK)"},
                    "destination": {"type": "string", "description": "Destination airport code (e.g. CDG)"},
                    "departure_date": {"type": "string", "description": "Departure date (YYYY-MM-DD)"},
                    "adults": {"type": "integer", "description": "Number of adult travelers", "default": 1},
                },
                "required": ["origin", "destination", "departure_date"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_flights":
        flights = await fetch_flights(
            origin=arguments["origin"],
            destination=arguments["destination"],
            departure_date=date.fromisoformat(arguments["departure_date"]),
            adults=arguments.get("adults", 1),
            api_key=settings.amadeus_api_key,
            api_secret=settings.amadeus_api_secret,
        )
        result = [f.model_dump(mode="json") for f in flights]
        return [TextContent(type="text", text=json.dumps(result))]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 3: Create MCP server for events**

Create `backend/app/mcp/events_server.py`:

```python
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
    return [
        Tool(
            name="search_events",
            description="Search for events in a city during specific dates",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                },
                "required": ["city", "start_date", "end_date"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_events":
        events = await fetch_events(
            city=arguments["city"],
            start_date=date.fromisoformat(arguments["start_date"]),
            end_date=date.fromisoformat(arguments["end_date"]),
            api_key=settings.ticketmaster_api_key,
        )
        result = [e.model_dump(mode="json") for e in events]
        return [TextContent(type="text", text=json.dumps(result, default=str))]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 4: Create MCP server for restaurants**

Create `backend/app/mcp/restaurant_server.py`:

```python
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
    return [
        Tool(
            name="search_restaurants",
            description="Search for top-rated restaurants in a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City or location"},
                    "cuisine": {"type": "string", "description": "Cuisine type filter (optional)"},
                },
                "required": ["location"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_restaurants":
        restaurants = await fetch_restaurants(
            location=arguments["location"],
            api_key=settings.yelp_api_key,
            cuisine=arguments.get("cuisine"),
        )
        result = [r.model_dump(mode="json") for r in restaurants]
        return [TextContent(type="text", text=json.dumps(result))]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 5: Commit**

```bash
git add backend/app/mcp/
git commit -m "feat: add MCP servers for weather, transport, events, and restaurants"
```

---

## Task 11: Supabase Database Schema

**Files:**
- Create: `supabase/migrations/001_initial_schema.sql`

- [ ] **Step 1: Create migration file**

Create `supabase/migrations/001_initial_schema.sql`:

```sql
-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Trips table
create table public.trips (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users(id) on delete cascade,
    request jsonb not null,
    result text,
    status text not null default 'pending' check (status in ('pending', 'planning', 'complete', 'error')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- Itineraries table
create table public.itineraries (
    id uuid primary key default uuid_generate_v4(),
    trip_id uuid references public.trips(id) on delete cascade,
    title text not null,
    data jsonb not null,
    total_cost numeric(10, 2) not null default 0,
    currency text not null default 'USD',
    created_at timestamptz not null default now()
);

-- Row Level Security
alter table public.trips enable row level security;
alter table public.itineraries enable row level security;

-- Policies: users can only see their own data
create policy "Users can view own trips"
    on public.trips for select
    using (auth.uid() = user_id);

create policy "Users can insert own trips"
    on public.trips for insert
    with check (auth.uid() = user_id);

create policy "Users can update own trips"
    on public.trips for update
    using (auth.uid() = user_id);

create policy "Users can view own itineraries"
    on public.itineraries for select
    using (trip_id in (select id from public.trips where user_id = auth.uid()));

-- Updated_at trigger
create or replace function public.update_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger trips_updated_at
    before update on public.trips
    for each row execute function public.update_updated_at();

-- Indexes
create index idx_trips_user_id on public.trips(user_id);
create index idx_trips_status on public.trips(status);
create index idx_itineraries_trip_id on public.itineraries(trip_id);
```

- [ ] **Step 2: Apply migration via Supabase MCP or CLI**

Run: `supabase db push` (if Supabase CLI is installed) or apply via Supabase dashboard.

- [ ] **Step 3: Commit**

```bash
git add supabase/
git commit -m "feat: add Supabase database schema for trips and itineraries with RLS"
```

---

## Task 12: Frontend Project Scaffolding

**Files:**
- Create: `frontend/` (via Vite scaffold)
- Modify: `frontend/package.json` (add dependencies)
- Create: `frontend/tailwind.config.ts`
- Modify: `frontend/src/index.css`
- Modify: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`

- [ ] **Step 1: Scaffold React + TypeScript project with Vite**

Run:
```bash
cd /Users/aarshghewde/FRAVEL && npm create vite@latest frontend -- --template react-ts
```
Expected: Vite project created in `frontend/`

- [ ] **Step 2: Install all dependencies**

Run:
```bash
cd frontend && npm install && npm install tailwindcss @tailwindcss/vite framer-motion zustand @supabase/supabase-js react-router-dom @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities lucide-react date-fns html2canvas jspdf
```
Expected: All packages installed

- [ ] **Step 3: Configure Tailwind**

Update `frontend/vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
```

Replace `frontend/src/index.css`:

```css
@import "tailwindcss";

@theme {
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;
  --color-primary-950: #172554;

  --color-accent-400: #f59e0b;
  --color-accent-500: #d97706;

  --color-surface-50: #f8fafc;
  --color-surface-100: #f1f5f9;
  --color-surface-800: #1e293b;
  --color-surface-900: #0f172a;
  --color-surface-950: #020617;

  --font-sans: "Inter", system-ui, -apple-system, sans-serif;
  --font-display: "Outfit", system-ui, sans-serif;
}

@layer base {
  html {
    scroll-behavior: smooth;
  }

  body {
    @apply bg-surface-50 text-surface-900 antialiased;
    @apply dark:bg-surface-950 dark:text-surface-50;
  }
}
```

- [ ] **Step 4: Create App.tsx with routing**

Replace `frontend/src/App.tsx`:

```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import Plan from "./pages/Plan";
import Itinerary from "./pages/Itinerary";
import History from "./pages/History";
import Auth from "./pages/Auth";
import Navbar from "./components/layout/Navbar";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/plan" element={<Plan />} />
            <Route path="/itinerary/:tripId" element={<Itinerary />} />
            <Route path="/history" element={<History />} />
            <Route path="/auth" element={<Auth />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
```

Replace `frontend/src/main.tsx`:

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

- [ ] **Step 5: Create placeholder pages so the app compiles**

Create `frontend/src/pages/Landing.tsx`:
```tsx
export default function Landing() {
  return <div className="p-8"><h1 className="text-4xl font-bold font-display">FRAVEL</h1></div>;
}
```

Create `frontend/src/pages/Plan.tsx`:
```tsx
export default function Plan() {
  return <div className="p-8">Plan</div>;
}
```

Create `frontend/src/pages/Itinerary.tsx`:
```tsx
export default function Itinerary() {
  return <div className="p-8">Itinerary</div>;
}
```

Create `frontend/src/pages/History.tsx`:
```tsx
export default function History() {
  return <div className="p-8">History</div>;
}
```

Create `frontend/src/pages/Auth.tsx`:
```tsx
export default function Auth() {
  return <div className="p-8">Auth</div>;
}
```

Create `frontend/src/components/layout/Navbar.tsx`:
```tsx
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="border-b border-surface-100 dark:border-surface-800 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="text-xl font-bold font-display text-primary-600">FRAVEL</Link>
        <div className="flex gap-6">
          <Link to="/plan" className="hover:text-primary-500 transition-colors">Plan Trip</Link>
          <Link to="/history" className="hover:text-primary-500 transition-colors">History</Link>
          <Link to="/auth" className="hover:text-primary-500 transition-colors">Sign In</Link>
        </div>
      </div>
    </nav>
  );
}
```

- [ ] **Step 6: Verify frontend compiles**

Run: `cd frontend && npm run build`
Expected: Build succeeds

- [ ] **Step 7: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold React frontend with Vite, Tailwind, routing, and design tokens"
```

---

## Task 13: Frontend TypeScript Types

**Files:**
- Create: `frontend/src/types/index.ts`

- [ ] **Step 1: Create shared types**

Create `frontend/src/types/index.ts`:

```typescript
export interface TripRequest {
  origin: string;
  destination: string;
  departure_date: string; // YYYY-MM-DD
  return_date: string;
  budget: number;
  interests: string[];
  travelers: number;
}

export interface TripResponse {
  trip_id: string;
  status: "pending" | "planning" | "complete" | "error";
  request: TripRequest;
  itinerary_id?: string;
}

export interface FlightOption {
  airline: string;
  flight_number: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  duration_minutes: number;
  price: number;
  currency: string;
  stops: number;
  cabin_class: string;
}

export interface EventOption {
  name: string;
  venue: string;
  date: string;
  category: string;
  price: number | null;
  currency: string;
  description: string;
  url: string;
  image_url: string;
}

export interface RestaurantOption {
  name: string;
  cuisine: string;
  rating: number;
  price_level: number;
  address: string;
  phone: string;
  url: string;
  image_url: string;
  review_count: number;
}

export interface DayWeather {
  date: string;
  temp_high_c: number;
  temp_low_c: number;
  condition: string;
  icon: string;
  humidity: number;
  wind_speed_kmh: number;
  precipitation_chance: number;
}

export interface Activity {
  time: string;
  title: string;
  description: string;
  category: "sightseeing" | "food" | "transport" | "event" | "free";
  cost: number;
  duration_minutes: number;
  location: string;
  latitude?: number;
  longitude?: number;
}

export interface DayPlan {
  date: string;
  title: string;
  activities: Activity[];
  weather?: DayWeather;
}

export interface Itinerary {
  trip_id: string;
  title: string;
  days: DayPlan[];
  total_cost: number;
  currency: string;
  summary: string;
}

export interface AgentStatus {
  agent: string;
  status: "idle" | "working" | "done" | "error" | "started" | "complete";
  detail: string;
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/types/
git commit -m "feat: add TypeScript interfaces matching backend models"
```

---

## Task 14: Frontend Lib — API Client, SSE, Supabase

**Files:**
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/lib/sse.ts`
- Create: `frontend/src/lib/supabase.ts`

- [ ] **Step 1: Create API client**

Create `frontend/src/lib/api.ts`:

```typescript
import type { TripRequest, TripResponse } from "../types";

const BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Request failed");
  }
  return res.json();
}

export async function createTrip(trip: TripRequest): Promise<TripResponse> {
  return request<TripResponse>("/trips", {
    method: "POST",
    body: JSON.stringify(trip),
  });
}

export async function getTrip(tripId: string): Promise<TripResponse> {
  return request<TripResponse>(`/trips/${tripId}`);
}
```

- [ ] **Step 2: Create SSE client**

Create `frontend/src/lib/sse.ts`:

```typescript
import type { AgentStatus } from "../types";

export function connectToTripStream(
  tripId: string,
  onStatus: (status: AgentStatus) => void,
  onComplete: (result: string) => void,
  onError: (error: string) => void
): () => void {
  const source = new EventSource(`/api/trips/${tripId}/stream`);

  source.addEventListener("agent_status", (e: MessageEvent) => {
    const data: AgentStatus = JSON.parse(e.data);
    onStatus(data);

    if (data.status === "complete" && data.agent === "system") {
      onComplete(data.detail);
      source.close();
    }
  });

  source.onerror = () => {
    onError("Connection lost. Retrying...");
  };

  return () => source.close();
}
```

- [ ] **Step 3: Create Supabase client**

Create `frontend/src/lib/supabase.ts`:

```typescript
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || "";
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || "";

export const supabase = createClient(supabaseUrl, supabaseKey);
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/lib/
git commit -m "feat: add API client, SSE helper, and Supabase client"
```

---

## Task 15: Frontend Store — Zustand Trip Store

**Files:**
- Create: `frontend/src/store/tripStore.ts`

- [ ] **Step 1: Create Zustand store**

Create `frontend/src/store/tripStore.ts`:

```typescript
import { create } from "zustand";
import type { TripRequest, TripResponse, AgentStatus, Itinerary } from "../types";
import { createTrip } from "../lib/api";
import { connectToTripStream } from "../lib/sse";

interface TripState {
  // Form state
  tripRequest: TripRequest | null;
  setTripRequest: (req: TripRequest) => void;

  // Planning state
  tripResponse: TripResponse | null;
  agentStatuses: AgentStatus[];
  isPlanning: boolean;
  error: string | null;

  // Result
  itinerary: Itinerary | null;

  // Actions
  startPlanning: () => Promise<void>;
  reset: () => void;
}

export const useTripStore = create<TripState>((set, get) => ({
  tripRequest: null,
  tripResponse: null,
  agentStatuses: [],
  isPlanning: false,
  error: null,
  itinerary: null,

  setTripRequest: (req) => set({ tripRequest: req }),

  startPlanning: async () => {
    const { tripRequest } = get();
    if (!tripRequest) return;

    set({ isPlanning: true, error: null, agentStatuses: [], itinerary: null });

    try {
      const response = await createTrip(tripRequest);
      set({ tripResponse: response });

      // Connect to SSE stream
      connectToTripStream(
        response.trip_id,
        (status) => {
          set((state) => {
            const existing = state.agentStatuses.findIndex(
              (s) => s.agent === status.agent
            );
            const updated = [...state.agentStatuses];
            if (existing >= 0) {
              updated[existing] = status;
            } else {
              updated.push(status);
            }
            return { agentStatuses: updated };
          });
        },
        (result) => {
          try {
            const itinerary = JSON.parse(result) as Itinerary;
            set({ itinerary, isPlanning: false });
          } catch {
            set({ isPlanning: false, error: "Failed to parse itinerary" });
          }
        },
        (error) => {
          set({ error });
        }
      );
    } catch (e) {
      set({ error: (e as Error).message, isPlanning: false });
    }
  },

  reset: () =>
    set({
      tripRequest: null,
      tripResponse: null,
      agentStatuses: [],
      isPlanning: false,
      error: null,
      itinerary: null,
    }),
}));
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/store/
git commit -m "feat: add Zustand trip store with SSE integration"
```

---

## Task 16: Frontend Hooks

**Files:**
- Create: `frontend/src/hooks/useAuth.ts`
- Create: `frontend/src/hooks/useTheme.ts`
- Create: `frontend/src/hooks/useAgentStatus.ts`

- [ ] **Step 1: Create hooks**

Create `frontend/src/hooks/useAuth.ts`:

```typescript
import { useEffect, useState } from "react";
import type { User } from "@supabase/supabase-js";
import { supabase } from "../lib/supabase";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
  };

  const signUp = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) throw error;
  };

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return { user, loading, signIn, signUp, signOut };
}
```

Create `frontend/src/hooks/useTheme.ts`:

```typescript
import { useEffect, useState } from "react";

export function useTheme() {
  const [dark, setDark] = useState(() => {
    if (typeof window === "undefined") return false;
    return (
      localStorage.getItem("theme") === "dark" ||
      (!localStorage.getItem("theme") &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    );
  });

  useEffect(() => {
    const root = document.documentElement;
    if (dark) {
      root.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      root.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [dark]);

  return { dark, toggle: () => setDark((d) => !d) };
}
```

Create `frontend/src/hooks/useAgentStatus.ts`:

```typescript
import { useTripStore } from "../store/tripStore";

const AGENT_ICONS: Record<string, string> = {
  "Transport Agent": "plane",
  "Events Agent": "ticket",
  "Restaurant Agent": "utensils",
  "Weather Agent": "cloud-sun",
  "Itinerary Compiler": "map",
  system: "cpu",
};

export function useAgentStatus() {
  const agentStatuses = useTripStore((s) => s.agentStatuses);
  const isPlanning = useTripStore((s) => s.isPlanning);

  const agents = agentStatuses
    .filter((s) => s.agent !== "system")
    .map((s) => ({
      ...s,
      icon: AGENT_ICONS[s.agent] || "bot",
    }));

  const progress = agents.length
    ? agents.filter((a) => a.status === "done").length / agents.length
    : 0;

  return { agents, progress, isPlanning };
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/hooks/
git commit -m "feat: add auth, theme, and agent status hooks"
```

---

## Task 17: Frontend UI Components

**Files:**
- Create: `frontend/src/components/ui/Button.tsx`
- Create: `frontend/src/components/ui/Input.tsx`
- Create: `frontend/src/components/ui/Card.tsx`
- Create: `frontend/src/components/ui/Badge.tsx`
- Create: `frontend/src/components/ui/DateRangePicker.tsx`
- Create: `frontend/src/components/ui/Select.tsx`
- Create: `frontend/src/components/ui/Slider.tsx`
- Create: `frontend/src/components/ui/LoadingSpinner.tsx`
- Create: `frontend/src/components/layout/ThemeToggle.tsx`
- Create: `frontend/src/components/layout/Footer.tsx`

> **Note to implementer:** Use @superpowers:frontend-design and @ui-ux-pro-max:ui-ux-pro-max skills when building these components. The designs below are structural — the skills will add the visual polish.

- [ ] **Step 1: Create UI primitives**

Create `frontend/src/components/ui/Button.tsx`:

```tsx
import { forwardRef, type ButtonHTMLAttributes } from "react";
import { motion } from "framer-motion";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
}

const variants = {
  primary:
    "bg-primary-600 text-white hover:bg-primary-700 shadow-lg shadow-primary-500/25",
  secondary:
    "bg-surface-100 text-surface-900 hover:bg-surface-200 dark:bg-surface-800 dark:text-surface-50 dark:hover:bg-surface-700",
  ghost: "text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-50 dark:hover:bg-surface-800",
};

const sizes = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-5 py-2.5 text-sm",
  lg: "px-7 py-3.5 text-base",
};

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", className = "", children, ...props }, ref) => (
    <motion.button
      ref={ref}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`
        inline-flex items-center justify-center gap-2 rounded-xl font-medium
        transition-colors focus-visible:outline-none focus-visible:ring-2
        focus-visible:ring-primary-500 focus-visible:ring-offset-2
        disabled:opacity-50 disabled:pointer-events-none
        ${variants[variant]} ${sizes[size]} ${className}
      `}
      {...(props as any)}
    >
      {children}
    </motion.button>
  )
);

Button.displayName = "Button";
export default Button;
```

Create `frontend/src/components/ui/Input.tsx`:

```tsx
import { forwardRef, type InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = "", ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          {label}
        </label>
      )}
      <input
        ref={ref}
        className={`
          w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5
          text-surface-900 placeholder:text-surface-400
          focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20
          dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50
          dark:placeholder:text-surface-500 dark:focus:border-primary-400
          transition-colors ${error ? "border-red-500" : ""} ${className}
        `}
        {...props}
      />
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  )
);

Input.displayName = "Input";
export default Input;
```

Create `frontend/src/components/ui/Card.tsx`:

```tsx
import { motion, type HTMLMotionProps } from "framer-motion";
import type { ReactNode } from "react";

interface CardProps extends HTMLMotionProps<"div"> {
  children: ReactNode;
  hover?: boolean;
  glass?: boolean;
}

export default function Card({ children, hover = false, glass = false, className = "", ...props }: CardProps) {
  return (
    <motion.div
      whileHover={hover ? { y: -2, scale: 1.01 } : undefined}
      className={`
        rounded-2xl border p-6
        ${glass
          ? "border-white/20 bg-white/10 backdrop-blur-xl dark:border-white/10 dark:bg-white/5"
          : "border-surface-200 bg-white dark:border-surface-800 dark:bg-surface-900"
        }
        shadow-sm ${hover ? "cursor-pointer" : ""} ${className}
      `}
      {...props}
    >
      {children}
    </motion.div>
  );
}
```

Create `frontend/src/components/ui/Badge.tsx`:

```tsx
import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  variant?: "default" | "success" | "warning" | "error" | "info";
  className?: string;
}

const colors = {
  default: "bg-surface-100 text-surface-700 dark:bg-surface-800 dark:text-surface-300",
  success: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  warning: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  error: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  info: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
};

export default function Badge({ children, variant = "default", className = "" }: BadgeProps) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${colors[variant]} ${className}`}>
      {children}
    </span>
  );
}
```

Create `frontend/src/components/ui/DateRangePicker.tsx`:

```tsx
import { useState } from "react";

interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  onStartChange: (date: string) => void;
  onEndChange: (date: string) => void;
}

export default function DateRangePicker({
  startDate,
  endDate,
  onStartChange,
  onEndChange,
}: DateRangePickerProps) {
  return (
    <div className="flex gap-3">
      <div className="flex-1 flex flex-col gap-1.5">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Departure
        </label>
        <input
          type="date"
          value={startDate}
          onChange={(e) => onStartChange(e.target.value)}
          className="w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5 text-surface-900 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50 transition-colors"
        />
      </div>
      <div className="flex-1 flex flex-col gap-1.5">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Return
        </label>
        <input
          type="date"
          value={endDate}
          min={startDate}
          onChange={(e) => onEndChange(e.target.value)}
          className="w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5 text-surface-900 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50 transition-colors"
        />
      </div>
    </div>
  );
}
```

Create `frontend/src/components/ui/Select.tsx`:

```tsx
import { forwardRef, type SelectHTMLAttributes } from "react";

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, options, className = "", ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          {label}
        </label>
      )}
      <select
        ref={ref}
        className={`w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5 text-surface-900 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50 transition-colors ${className}`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  )
);

Select.displayName = "Select";
export default Select;
```

Create `frontend/src/components/ui/Slider.tsx`:

```tsx
interface SliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  format?: (value: number) => string;
  onChange: (value: number) => void;
}

export default function Slider({ label, value, min, max, step = 1, format, onChange }: SliderProps) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">{label}</label>
        <span className="text-sm font-semibold text-primary-600 dark:text-primary-400">
          {format ? format(value) : value}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-primary-600"
      />
    </div>
  );
}
```

Create `frontend/src/components/ui/LoadingSpinner.tsx`:

```tsx
import { motion } from "framer-motion";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
}

const sizes = { sm: "h-4 w-4", md: "h-8 w-8", lg: "h-12 w-12" };

export default function LoadingSpinner({ size = "md" }: LoadingSpinnerProps) {
  return (
    <motion.div
      className={`${sizes[size]} rounded-full border-2 border-surface-200 border-t-primary-600 dark:border-surface-700 dark:border-t-primary-400`}
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    />
  );
}
```

- [ ] **Step 2: Create layout components**

Create `frontend/src/components/layout/ThemeToggle.tsx`:

```tsx
import { motion } from "framer-motion";
import { useTheme } from "../../hooks/useTheme";
import { Sun, Moon } from "lucide-react";

export default function ThemeToggle() {
  const { dark, toggle } = useTheme();
  return (
    <motion.button
      whileTap={{ scale: 0.9 }}
      onClick={toggle}
      className="rounded-xl p-2 text-surface-500 hover:bg-surface-100 hover:text-surface-700 dark:hover:bg-surface-800 dark:hover:text-surface-300 transition-colors"
      aria-label="Toggle theme"
    >
      {dark ? <Sun size={20} /> : <Moon size={20} />}
    </motion.button>
  );
}
```

Create `frontend/src/components/layout/Footer.tsx`:

```tsx
export default function Footer() {
  return (
    <footer className="border-t border-surface-100 dark:border-surface-800 py-6 px-6 text-center text-sm text-surface-500">
      FRAVEL — AI-Powered Travel Planning
    </footer>
  );
}
```

- [ ] **Step 3: Update Navbar to include ThemeToggle**

Replace `frontend/src/components/layout/Navbar.tsx`:

```tsx
import { Link } from "react-router-dom";
import { Plane } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-surface-100 bg-white/80 backdrop-blur-xl dark:border-surface-800 dark:bg-surface-950/80">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold font-display text-primary-600">
          <Plane size={24} />
          FRAVEL
        </Link>
        <div className="flex items-center gap-6">
          <Link to="/plan" className="text-sm font-medium hover:text-primary-500 transition-colors">
            Plan Trip
          </Link>
          <Link to="/history" className="text-sm font-medium hover:text-primary-500 transition-colors">
            History
          </Link>
          <Link to="/auth" className="text-sm font-medium hover:text-primary-500 transition-colors">
            Sign In
          </Link>
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
```

- [ ] **Step 4: Verify frontend compiles**

Run: `cd frontend && npm run build`
Expected: Build succeeds

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/
git commit -m "feat: add polished UI components - buttons, inputs, cards, badges, date picker, theme toggle"
```

---

## Task 18: Frontend — Agent Status Panel & Progress Ring

**Files:**
- Create: `frontend/src/components/agents/AgentStatusPanel.tsx`
- Create: `frontend/src/components/agents/AgentProgressRing.tsx`

- [ ] **Step 1: Create AgentProgressRing**

Create `frontend/src/components/agents/AgentProgressRing.tsx`:

```tsx
import { motion } from "framer-motion";

interface AgentProgressRingProps {
  progress: number; // 0 to 1
  size?: number;
}

export default function AgentProgressRing({ progress, size = 120 }: AgentProgressRingProps) {
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - progress * circumference;

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
          className="stroke-surface-200 dark:stroke-surface-800"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          className="stroke-primary-500"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          strokeDasharray={circumference}
        />
      </svg>
      <span className="absolute text-2xl font-bold font-display text-primary-600 dark:text-primary-400">
        {Math.round(progress * 100)}%
      </span>
    </div>
  );
}
```

- [ ] **Step 2: Create AgentStatusPanel**

Create `frontend/src/components/agents/AgentStatusPanel.tsx`:

```tsx
import { motion, AnimatePresence } from "framer-motion";
import { Plane, Ticket, UtensilsCrossed, CloudSun, Map, Loader2, CheckCircle2 } from "lucide-react";
import { useAgentStatus } from "../../hooks/useAgentStatus";
import AgentProgressRing from "./AgentProgressRing";

const ICONS: Record<string, React.ReactNode> = {
  plane: <Plane size={20} />,
  ticket: <Ticket size={20} />,
  utensils: <UtensilsCrossed size={20} />,
  "cloud-sun": <CloudSun size={20} />,
  map: <Map size={20} />,
};

export default function AgentStatusPanel() {
  const { agents, progress, isPlanning } = useAgentStatus();

  if (!isPlanning && agents.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-surface-200 bg-white p-6 shadow-lg dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="flex items-center gap-6">
        <AgentProgressRing progress={progress} />
        <div className="flex-1 space-y-3">
          <h3 className="text-lg font-semibold font-display">AI Agents Working</h3>
          <AnimatePresence mode="popLayout">
            {agents.map((agent) => (
              <motion.div
                key={agent.agent}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3"
              >
                <span className={agent.status === "done" ? "text-emerald-500" : "text-primary-500"}>
                  {ICONS[agent.icon] || <Map size={20} />}
                </span>
                <span className="flex-1 text-sm font-medium">{agent.agent}</span>
                {agent.status === "working" ? (
                  <Loader2 size={16} className="animate-spin text-primary-500" />
                ) : agent.status === "done" ? (
                  <CheckCircle2 size={16} className="text-emerald-500" />
                ) : null}
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/agents/
git commit -m "feat: add agent status panel with animated progress ring"
```

---

## Task 19: Frontend — Trip Form Component

**Files:**
- Create: `frontend/src/components/trip/TripForm.tsx`

- [ ] **Step 1: Create TripForm**

Create `frontend/src/components/trip/TripForm.tsx`:

```tsx
import { useState } from "react";
import { motion } from "framer-motion";
import { MapPin, Calendar, DollarSign, Users, Sparkles } from "lucide-react";
import Input from "../ui/Input";
import Button from "../ui/Button";
import DateRangePicker from "../ui/DateRangePicker";
import Slider from "../ui/Slider";
import { useTripStore } from "../../store/tripStore";

const INTEREST_OPTIONS = [
  "Museums", "Food", "Nightlife", "Nature", "Shopping",
  "History", "Art", "Music", "Sports", "Adventure",
  "Beach", "Architecture", "Photography", "Local Culture",
];

export default function TripForm() {
  const { setTripRequest, startPlanning, isPlanning } = useTripStore();
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [budget, setBudget] = useState(3000);
  const [travelers, setTravelers] = useState(1);
  const [interests, setInterests] = useState<string[]>([]);

  const toggleInterest = (interest: string) => {
    setInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const request = {
      origin,
      destination,
      departure_date: startDate,
      return_date: endDate,
      budget,
      interests: interests.map((i) => i.toLowerCase()),
      travelers,
    };
    setTripRequest(request);
    await startPlanning();
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mx-auto max-w-2xl space-y-6 rounded-3xl border border-surface-200 bg-white p-8 shadow-xl dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="text-center">
        <h2 className="text-2xl font-bold font-display">Plan Your Trip</h2>
        <p className="mt-1 text-surface-500">Our AI agents will craft the perfect itinerary</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="relative">
          <MapPin size={16} className="absolute left-3 top-9 text-surface-400" />
          <Input
            label="From"
            placeholder="New York"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            className="pl-9"
            required
          />
        </div>
        <div className="relative">
          <MapPin size={16} className="absolute left-3 top-9 text-primary-500" />
          <Input
            label="To"
            placeholder="Paris"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            className="pl-9"
            required
          />
        </div>
      </div>

      <DateRangePicker
        startDate={startDate}
        endDate={endDate}
        onStartChange={setStartDate}
        onEndChange={setEndDate}
      />

      <Slider
        label="Budget"
        value={budget}
        min={500}
        max={20000}
        step={100}
        format={(v) => `$${v.toLocaleString()}`}
        onChange={setBudget}
      />

      <div className="flex flex-col gap-1.5">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          <Users size={14} className="mr-1 inline" />
          Travelers: {travelers}
        </label>
        <input
          type="range"
          min={1}
          max={10}
          value={travelers}
          onChange={(e) => setTravelers(Number(e.target.value))}
          className="accent-primary-600"
        />
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">Interests</label>
        <div className="flex flex-wrap gap-2">
          {INTEREST_OPTIONS.map((interest) => (
            <motion.button
              key={interest}
              type="button"
              whileTap={{ scale: 0.95 }}
              onClick={() => toggleInterest(interest)}
              className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
                interests.includes(interest)
                  ? "bg-primary-600 text-white"
                  : "bg-surface-100 text-surface-600 hover:bg-surface-200 dark:bg-surface-800 dark:text-surface-400"
              }`}
            >
              {interest}
            </motion.button>
          ))}
        </div>
      </div>

      <Button
        type="submit"
        size="lg"
        className="w-full"
        disabled={isPlanning || !origin || !destination || !startDate || !endDate}
      >
        <Sparkles size={18} />
        {isPlanning ? "Planning..." : "Plan My Trip"}
      </Button>
    </motion.form>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/trip/TripForm.tsx
git commit -m "feat: add trip form with origin, destination, dates, budget, interests"
```

---

## Task 20: Frontend — Itinerary Card Components

**Files:**
- Create: `frontend/src/components/itinerary/FlightCard.tsx`
- Create: `frontend/src/components/itinerary/RestaurantCard.tsx`
- Create: `frontend/src/components/itinerary/EventCard.tsx`
- Create: `frontend/src/components/itinerary/WeatherBadge.tsx`
- Create: `frontend/src/components/itinerary/ActivityCard.tsx`
- Create: `frontend/src/components/itinerary/DayColumn.tsx`
- Create: `frontend/src/components/itinerary/ItineraryView.tsx`
- Create: `frontend/src/components/itinerary/ExportPDF.tsx`

- [ ] **Step 1: Create card components**

Create `frontend/src/components/itinerary/WeatherBadge.tsx`:

```tsx
import { CloudSun, Cloud, CloudRain, Sun, Snowflake } from "lucide-react";
import type { DayWeather } from "../../types";

const WEATHER_ICONS: Record<string, React.ReactNode> = {
  Clear: <Sun size={16} className="text-amber-500" />,
  Clouds: <Cloud size={16} className="text-surface-400" />,
  Rain: <CloudRain size={16} className="text-blue-500" />,
  Snow: <Snowflake size={16} className="text-blue-300" />,
};

export default function WeatherBadge({ weather }: { weather: DayWeather }) {
  return (
    <div className="flex items-center gap-2 rounded-lg bg-surface-50 px-3 py-1.5 text-xs dark:bg-surface-800">
      {WEATHER_ICONS[weather.condition] || <CloudSun size={16} />}
      <span>{weather.temp_low_c}°-{weather.temp_high_c}°C</span>
      <span className="text-surface-400">{weather.precipitation_chance}% rain</span>
    </div>
  );
}
```

Create `frontend/src/components/itinerary/ActivityCard.tsx`:

```tsx
import { motion } from "framer-motion";
import { Clock, MapPin, DollarSign } from "lucide-react";
import Badge from "../ui/Badge";
import type { Activity } from "../../types";

const CATEGORY_COLORS: Record<string, "info" | "success" | "warning" | "default" | "error"> = {
  sightseeing: "info",
  food: "warning",
  transport: "default",
  event: "success",
  free: "default",
};

export default function ActivityCard({ activity }: { activity: Activity }) {
  return (
    <motion.div
      whileHover={{ x: 4 }}
      className="flex gap-4 rounded-xl border border-surface-100 bg-white p-4 dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="flex flex-col items-center">
        <span className="text-sm font-bold text-primary-600 dark:text-primary-400">{activity.time}</span>
        <div className="mt-1 h-full w-px bg-surface-200 dark:bg-surface-700" />
      </div>
      <div className="flex-1 space-y-1">
        <div className="flex items-start justify-between">
          <h4 className="font-semibold">{activity.title}</h4>
          <Badge variant={CATEGORY_COLORS[activity.category] || "default"}>
            {activity.category}
          </Badge>
        </div>
        <p className="text-sm text-surface-500">{activity.description}</p>
        <div className="flex gap-4 text-xs text-surface-400">
          <span className="flex items-center gap-1">
            <Clock size={12} /> {activity.duration_minutes}min
          </span>
          {activity.location && (
            <span className="flex items-center gap-1">
              <MapPin size={12} /> {activity.location}
            </span>
          )}
          {activity.cost > 0 && (
            <span className="flex items-center gap-1">
              <DollarSign size={12} /> ${activity.cost}
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
}
```

Create `frontend/src/components/itinerary/FlightCard.tsx`:

```tsx
import { Plane, Clock, ArrowRight } from "lucide-react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import type { FlightOption } from "../../types";

export default function FlightCard({ flight }: { flight: FlightOption }) {
  const dep = new Date(flight.departure_time);
  const arr = new Date(flight.arrival_time);

  return (
    <Card hover className="flex items-center gap-4">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
        <Plane size={24} />
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="font-semibold">{flight.airline} {flight.flight_number}</span>
          <Badge variant={flight.stops === 0 ? "success" : "warning"}>
            {flight.stops === 0 ? "Direct" : `${flight.stops} stop(s)`}
          </Badge>
        </div>
        <div className="flex items-center gap-2 text-sm text-surface-500">
          <span>{flight.origin} {dep.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
          <ArrowRight size={14} />
          <span>{flight.destination} {arr.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
          <span className="flex items-center gap-1"><Clock size={12} /> {Math.floor(flight.duration_minutes / 60)}h {flight.duration_minutes % 60}m</span>
        </div>
      </div>
      <div className="text-right">
        <div className="text-xl font-bold text-primary-600 dark:text-primary-400">${flight.price}</div>
        <div className="text-xs text-surface-400">{flight.cabin_class}</div>
      </div>
    </Card>
  );
}
```

Create `frontend/src/components/itinerary/RestaurantCard.tsx`:

```tsx
import { UtensilsCrossed, Star, MapPin } from "lucide-react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import type { RestaurantOption } from "../../types";

export default function RestaurantCard({ restaurant }: { restaurant: RestaurantOption }) {
  return (
    <Card hover className="flex gap-4">
      {restaurant.image_url ? (
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="h-24 w-24 rounded-xl object-cover"
        />
      ) : (
        <div className="flex h-24 w-24 items-center justify-center rounded-xl bg-amber-100 dark:bg-amber-900/30">
          <UtensilsCrossed size={32} className="text-amber-600" />
        </div>
      )}
      <div className="flex-1 space-y-1">
        <h4 className="font-semibold">{restaurant.name}</h4>
        <div className="flex items-center gap-2">
          <Badge variant="warning">{restaurant.cuisine}</Badge>
          <span className="flex items-center gap-1 text-sm text-amber-500">
            <Star size={14} fill="currentColor" /> {restaurant.rating}
          </span>
          <span className="text-sm text-surface-400">
            {"$".repeat(restaurant.price_level)}
          </span>
        </div>
        <p className="flex items-center gap-1 text-xs text-surface-400">
          <MapPin size={12} /> {restaurant.address}
        </p>
      </div>
    </Card>
  );
}
```

Create `frontend/src/components/itinerary/EventCard.tsx`:

```tsx
import { Ticket, Calendar, MapPin } from "lucide-react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import type { EventOption } from "../../types";

export default function EventCard({ event }: { event: EventOption }) {
  const date = new Date(event.date);

  return (
    <Card hover className="flex gap-4">
      {event.image_url ? (
        <img
          src={event.image_url}
          alt={event.name}
          className="h-24 w-24 rounded-xl object-cover"
        />
      ) : (
        <div className="flex h-24 w-24 items-center justify-center rounded-xl bg-emerald-100 dark:bg-emerald-900/30">
          <Ticket size={32} className="text-emerald-600" />
        </div>
      )}
      <div className="flex-1 space-y-1">
        <h4 className="font-semibold">{event.name}</h4>
        <div className="flex items-center gap-2">
          <Badge variant="success">{event.category}</Badge>
          {event.price != null && (
            <span className="text-sm font-semibold text-primary-600">${event.price}</span>
          )}
        </div>
        <div className="flex gap-3 text-xs text-surface-400">
          <span className="flex items-center gap-1">
            <Calendar size={12} /> {date.toLocaleDateString()}
          </span>
          <span className="flex items-center gap-1">
            <MapPin size={12} /> {event.venue}
          </span>
        </div>
      </div>
    </Card>
  );
}
```

- [ ] **Step 2: Create DayColumn with drag-and-drop**

Create `frontend/src/components/itinerary/DayColumn.tsx`:

```tsx
import { motion } from "framer-motion";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { GripVertical } from "lucide-react";
import ActivityCard from "./ActivityCard";
import WeatherBadge from "./WeatherBadge";
import type { DayPlan } from "../../types";

interface DayColumnProps {
  day: DayPlan;
  index: number;
}

export default function DayColumn({ day, index }: DayColumnProps) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
    id: day.date,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const dateObj = new Date(day.date);

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="space-y-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            {...attributes}
            {...listeners}
            className="cursor-grab text-surface-400 hover:text-surface-600 dark:hover:text-surface-300"
          >
            <GripVertical size={20} />
          </button>
          <div>
            <h3 className="text-lg font-bold font-display">{day.title}</h3>
            <p className="text-sm text-surface-500">
              {dateObj.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
            </p>
          </div>
        </div>
        {day.weather && <WeatherBadge weather={day.weather} />}
      </div>
      <div className="space-y-3">
        {day.activities.map((activity, i) => (
          <ActivityCard key={`${day.date}-${i}`} activity={activity} />
        ))}
      </div>
    </motion.div>
  );
}
```

- [ ] **Step 3: Create ItineraryView**

Create `frontend/src/components/itinerary/ItineraryView.tsx`:

```tsx
import { motion } from "framer-motion";
import { DndContext, closestCenter } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { DollarSign, Calendar } from "lucide-react";
import DayColumn from "./DayColumn";
import ExportPDF from "./ExportPDF";
import type { Itinerary } from "../../types";

interface ItineraryViewProps {
  itinerary: Itinerary;
}

export default function ItineraryView({ itinerary }: ItineraryViewProps) {
  return (
    <div className="mx-auto max-w-4xl space-y-8" id="itinerary-content">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold font-display">{itinerary.title}</h1>
        {itinerary.summary && (
          <p className="mt-2 text-surface-500 max-w-2xl mx-auto">{itinerary.summary}</p>
        )}
        <div className="mt-4 flex items-center justify-center gap-6">
          <span className="flex items-center gap-2 text-sm">
            <Calendar size={16} className="text-primary-500" />
            {itinerary.days.length} days
          </span>
          <span className="flex items-center gap-2 text-sm">
            <DollarSign size={16} className="text-emerald-500" />
            ${itinerary.total_cost.toLocaleString()} {itinerary.currency}
          </span>
          <ExportPDF />
        </div>
      </motion.div>

      <DndContext collisionDetection={closestCenter}>
        <SortableContext items={itinerary.days.map((d) => d.date)} strategy={verticalListSortingStrategy}>
          <div className="space-y-10">
            {itinerary.days.map((day, i) => (
              <DayColumn key={day.date} day={day} index={i} />
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );
}
```

- [ ] **Step 4: Create ExportPDF**

Create `frontend/src/components/itinerary/ExportPDF.tsx`:

```tsx
import { Download } from "lucide-react";
import Button from "../ui/Button";

export default function ExportPDF() {
  const handleExport = async () => {
    const element = document.getElementById("itinerary-content");
    if (!element) return;

    const html2canvas = (await import("html2canvas")).default;
    const { jsPDF } = await import("jspdf");

    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const imgWidth = 210;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
    heightLeft -= 297;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
      heightLeft -= 297;
    }

    pdf.save("fravel-itinerary.pdf");
  };

  return (
    <Button variant="secondary" size="sm" onClick={handleExport}>
      <Download size={14} />
      Export PDF
    </Button>
  );
}
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/itinerary/
git commit -m "feat: add itinerary view with day columns, activity/flight/restaurant/event cards, weather badges, drag-and-drop, and PDF export"
```

---

## Task 21: Frontend — Landing Page

**Files:**
- Modify: `frontend/src/pages/Landing.tsx`

> **Note to implementer:** Use @frontend-design:frontend-design and @ui-ux-pro-max:ui-ux-pro-max for visual polish.

- [ ] **Step 1: Build Landing page**

Replace `frontend/src/pages/Landing.tsx`:

```tsx
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Plane, MapPin, Sparkles, Utensils, Cloud, Calendar } from "lucide-react";
import Button from "../components/ui/Button";

const features = [
  { icon: <Plane size={24} />, title: "Smart Flights", desc: "AI finds the best routes and prices" },
  { icon: <Calendar size={24} />, title: "Local Events", desc: "Discover festivals, concerts, tours" },
  { icon: <Utensils size={24} />, title: "Top Restaurants", desc: "Curated dining with real reviews" },
  { icon: <Cloud size={24} />, title: "Weather Aware", desc: "Plans adapt to forecasted conditions" },
  { icon: <MapPin size={24} />, title: "Day-by-Day", desc: "Optimized itineraries with maps" },
  { icon: <Sparkles size={24} />, title: "AI Powered", desc: "5 specialized agents work for you" },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="overflow-hidden">
      {/* Hero */}
      <section className="relative flex min-h-[80vh] items-center justify-center px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-accent-400/10 dark:from-surface-950 dark:via-surface-950 dark:to-primary-950/30" />
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute h-1 w-1 rounded-full bg-primary-400/20"
              style={{ left: `${Math.random() * 100}%`, top: `${Math.random() * 100}%` }}
              animate={{ y: [0, -30, 0], opacity: [0.2, 0.8, 0.2] }}
              transition={{ duration: 3 + Math.random() * 4, repeat: Infinity, delay: Math.random() * 2 }}
            />
          ))}
        </div>
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10 text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", delay: 0.2 }}
            className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary-600 text-white shadow-2xl shadow-primary-500/40"
          >
            <Plane size={40} />
          </motion.div>
          <h1 className="text-5xl font-bold font-display tracking-tight sm:text-7xl">
            <span className="text-primary-600">FR</span>AVEL
          </h1>
          <p className="mt-4 text-lg text-surface-500 sm:text-xl max-w-xl mx-auto">
            AI agents research flights, events, restaurants, and weather — then build your perfect itinerary.
          </p>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-8 flex gap-4 justify-center"
          >
            <Button size="lg" onClick={() => navigate("/plan")}>
              <Sparkles size={18} />
              Plan a Trip
            </Button>
            <Button variant="secondary" size="lg" onClick={() => navigate("/auth")}>
              Sign In
            </Button>
          </motion.div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-6xl px-6 py-24">
        <h2 className="text-center text-3xl font-bold font-display">How It Works</h2>
        <p className="mt-2 text-center text-surface-500">Five specialized AI agents work together</p>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="rounded-2xl border border-surface-200 bg-white p-6 dark:border-surface-800 dark:bg-surface-900"
            >
              <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
                {f.icon}
              </div>
              <h3 className="font-semibold">{f.title}</h3>
              <p className="mt-1 text-sm text-surface-500">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
```

- [ ] **Step 2: Verify frontend compiles**

Run: `cd frontend && npm run build`
Expected: Build succeeds

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/Landing.tsx
git commit -m "feat: add polished landing page with hero section, animated particles, and feature grid"
```

---

## Task 22: Frontend — Plan Page

**Files:**
- Modify: `frontend/src/pages/Plan.tsx`

- [ ] **Step 1: Build Plan page**

Replace `frontend/src/pages/Plan.tsx`:

```tsx
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import TripForm from "../components/trip/TripForm";
import AgentStatusPanel from "../components/agents/AgentStatusPanel";
import ItineraryView from "../components/itinerary/ItineraryView";
import { useTripStore } from "../store/tripStore";

export default function Plan() {
  const { itinerary, isPlanning, tripResponse } = useTripStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (itinerary && tripResponse) {
      navigate(`/itinerary/${tripResponse.trip_id}`);
    }
  }, [itinerary, tripResponse, navigate]);

  return (
    <div className="mx-auto max-w-4xl px-6 py-12 space-y-8">
      {!isPlanning && !itinerary && <TripForm />}
      {isPlanning && <AgentStatusPanel />}
      {itinerary && <ItineraryView itinerary={itinerary} />}
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/Plan.tsx
git commit -m "feat: add plan page with trip form, agent status, and itinerary view"
```

---

## Task 23: Frontend — Itinerary Page

**Files:**
- Modify: `frontend/src/pages/Itinerary.tsx`

- [ ] **Step 1: Build Itinerary page**

Replace `frontend/src/pages/Itinerary.tsx`:

```tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ItineraryView from "../components/itinerary/ItineraryView";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { useTripStore } from "../store/tripStore";
import { getTrip } from "../lib/api";
import type { Itinerary as ItineraryType } from "../types";

export default function Itinerary() {
  const { tripId } = useParams<{ tripId: string }>();
  const storeItinerary = useTripStore((s) => s.itinerary);
  const [fetchedItinerary, setFetchedItinerary] = useState<ItineraryType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const itinerary = storeItinerary || fetchedItinerary;

  useEffect(() => {
    if (!storeItinerary && tripId) {
      getTrip(tripId)
        .then((trip) => {
          if (trip.status === "complete") {
            // Itinerary data would be stored in Supabase; fetch it
            // For now, show a message to re-plan
            setError("Itinerary data not in memory. Please re-plan your trip.");
          }
        })
        .catch(() => setError("Trip not found"));
    }
  }, [storeItinerary, tripId]);

  if (error) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <p className="text-surface-500">{error}</p>
      </div>
    );
  }

  if (!itinerary) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center space-y-4">
          <LoadingSpinner size="lg" />
          <p className="text-surface-500">Loading itinerary...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-6 py-12">
      <ItineraryView itinerary={itinerary} />
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/Itinerary.tsx
git commit -m "feat: add itinerary page with loading state"
```

---

## Task 24: Frontend — Auth Page

**Files:**
- Modify: `frontend/src/pages/Auth.tsx`

- [ ] **Step 1: Build Auth page**

Replace `frontend/src/pages/Auth.tsx`:

```tsx
import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Mail, Lock, LogIn } from "lucide-react";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import { useAuth } from "../hooks/useAuth";

export default function Auth() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { signIn, signUp } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (isSignUp) {
        await signUp(email, password);
      } else {
        await signIn(email, password);
      }
      navigate("/plan");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[70vh] items-center justify-center px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <Card className="space-y-6">
          <div className="text-center">
            <h2 className="text-2xl font-bold font-display">
              {isSignUp ? "Create Account" : "Welcome Back"}
            </h2>
            <p className="mt-1 text-surface-500">
              {isSignUp ? "Start planning your next adventure" : "Sign in to your account"}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <Mail size={16} className="absolute left-3 top-9 text-surface-400" />
              <Input
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="pl-9"
                required
              />
            </div>
            <div className="relative">
              <Lock size={16} className="absolute left-3 top-9 text-surface-400" />
              <Input
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="pl-9"
                required
              />
            </div>

            {error && (
              <p className="text-sm text-red-500 text-center">{error}</p>
            )}

            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              <LogIn size={18} />
              {loading ? "Loading..." : isSignUp ? "Sign Up" : "Sign In"}
            </Button>
          </form>

          <p className="text-center text-sm text-surface-500">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
            <button
              onClick={() => setIsSignUp(!isSignUp)}
              className="font-medium text-primary-600 hover:underline"
            >
              {isSignUp ? "Sign In" : "Sign Up"}
            </button>
          </p>
        </Card>
      </motion.div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/pages/Auth.tsx
git commit -m "feat: add auth page with sign in/sign up toggle"
```

---

## Task 25: Frontend — History Page

**Files:**
- Modify: `frontend/src/pages/History.tsx`
- Create: `frontend/src/components/trip/TripCard.tsx`
- Create: `frontend/src/components/trip/TripHistory.tsx`

- [ ] **Step 1: Create TripCard**

Create `frontend/src/components/trip/TripCard.tsx`:

```tsx
import { motion } from "framer-motion";
import { MapPin, Calendar, DollarSign, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Badge from "../ui/Badge";

interface TripCardProps {
  tripId: string;
  origin: string;
  destination: string;
  departureDate: string;
  returnDate: string;
  budget: number;
  status: string;
}

export default function TripCard({
  tripId, origin, destination, departureDate, returnDate, budget, status,
}: TripCardProps) {
  const navigate = useNavigate();

  return (
    <motion.div
      whileHover={{ y: -2 }}
      onClick={() => navigate(`/itinerary/${tripId}`)}
      className="cursor-pointer rounded-2xl border border-surface-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:border-surface-800 dark:bg-surface-900"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-lg font-semibold font-display">
          <MapPin size={18} className="text-primary-500" />
          {origin} <ArrowRight size={16} /> {destination}
        </div>
        <Badge variant={status === "complete" ? "success" : status === "error" ? "error" : "info"}>
          {status}
        </Badge>
      </div>
      <div className="mt-3 flex gap-4 text-sm text-surface-500">
        <span className="flex items-center gap-1">
          <Calendar size={14} /> {departureDate} - {returnDate}
        </span>
        <span className="flex items-center gap-1">
          <DollarSign size={14} /> ${budget.toLocaleString()}
        </span>
      </div>
    </motion.div>
  );
}
```

Create `frontend/src/components/trip/TripHistory.tsx`:

```tsx
import TripCard from "./TripCard";

interface Trip {
  id: string;
  request: {
    origin: string;
    destination: string;
    departure_date: string;
    return_date: string;
    budget: number;
  };
  status: string;
}

export default function TripHistory({ trips }: { trips: Trip[] }) {
  if (trips.length === 0) {
    return (
      <div className="text-center py-12 text-surface-500">
        No trips yet. Start planning your first adventure!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {trips.map((trip) => (
        <TripCard
          key={trip.id}
          tripId={trip.id}
          origin={trip.request.origin}
          destination={trip.request.destination}
          departureDate={trip.request.departure_date}
          returnDate={trip.request.return_date}
          budget={trip.request.budget}
          status={trip.status}
        />
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Build History page**

Replace `frontend/src/pages/History.tsx`:

```tsx
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { History as HistoryIcon } from "lucide-react";
import TripHistory from "../components/trip/TripHistory";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { supabase } from "../lib/supabase";

export default function History() {
  const [trips, setTrips] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTrips() {
      const { data } = await supabase
        .from("trips")
        .select("*")
        .order("created_at", { ascending: false });
      setTrips(data || []);
      setLoading(false);
    }
    loadTrips();
  }, []);

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="space-y-6"
      >
        <div className="flex items-center gap-3">
          <HistoryIcon size={28} className="text-primary-600" />
          <h1 className="text-3xl font-bold font-display">Trip History</h1>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <TripHistory trips={trips} />
        )}
      </motion.div>
    </div>
  );
}
```

- [ ] **Step 3: Verify frontend compiles**

Run: `cd frontend && npm run build`
Expected: Build succeeds

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/History.tsx frontend/src/components/trip/
git commit -m "feat: add trip history page with trip cards"
```

---

## Task 26: Run All Backend Tests

- [ ] **Step 1: Run full test suite**

Run: `cd backend && pytest -v`
Expected: All tests PASS

- [ ] **Step 2: Fix any failures**

If any tests fail, fix them before proceeding.

- [ ] **Step 3: Commit any fixes**

```bash
git add -A
git commit -m "fix: resolve test failures"
```

---

## Task 27: Final Frontend Build Verification

- [ ] **Step 1: Full frontend build**

Run: `cd frontend && npm run build`
Expected: Build succeeds with no errors

- [ ] **Step 2: Fix any TypeScript or build errors**

- [ ] **Step 3: Commit any fixes**

```bash
git add -A
git commit -m "fix: resolve build errors"
```

---

## Task 28: Root-Level Configuration

**Files:**
- Create: `.env.example` (root)

> **Note:** `.gitignore` was already created in Task 1 Step 0.

- [ ] **Step 1: Create root .env.example**

Create `.env.example`:

```env
# Copy to .env and fill in values

# LLM (Ollama - no API key needed)
OLLAMA_MODEL=
OLLAMA_BASE_URL=http://localhost:11434

# External APIs
AMADEUS_API_KEY=
AMADEUS_API_SECRET=
OPENWEATHER_API_KEY=
YELP_API_KEY=
TICKETMASTER_API_KEY=

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# Frontend (also set in frontend/.env)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

- [ ] **Step 2: Commit**

```bash
git add .env.example
git commit -m "chore: add root env example"
```

---

## Summary

| Task | Description | Est. Steps |
|------|-------------|------------|
| 1 | Backend scaffolding (FastAPI + config) | 10 |
| 2 | Backend data models (Pydantic) | 5 |
| 3 | Weather tool (OpenWeather) | 5 |
| 4 | Transport tool (Amadeus) | 5 |
| 5 | Events tool (Ticketmaster) | 5 |
| 6 | Restaurant tool (Yelp) | 5 |
| 7 | CrewAI agents + crew | 5 |
| 8 | Supabase client + planner service | 4 |
| 9 | API routes (trips, auth, SSE) | 6 |
| 10 | MCP servers (4 servers) | 5 |
| 11 | Supabase DB schema | 3 |
| 12 | Frontend scaffolding | 7 |
| 13 | TypeScript types | 2 |
| 14 | Frontend lib (API, SSE, Supabase) | 4 |
| 15 | Zustand store | 2 |
| 16 | Frontend hooks | 2 |
| 17 | UI components (10 components) | 5 |
| 18 | Agent status panel | 3 |
| 19 | Trip form | 2 |
| 20 | Itinerary cards + view + PDF export | 5 |
| 21 | Landing page | 3 |
| 22 | Plan page | 2 |
| 23 | Itinerary page | 2 |
| 24 | Auth page | 2 |
| 25 | History page | 4 |
| 26 | Backend test suite | 3 |
| 27 | Frontend build verification | 3 |
| 28 | Root config | 3 |

**Total: 28 tasks, ~112 steps**

### Parallelization Strategy

These task groups can run in parallel via subagents:

- **Group A (Backend Tools):** Tasks 3, 4, 5, 6 (all independent API wrappers)
- **Group B (Frontend Components):** Tasks 17, 18, 19, 20 (all independent React components)
- **Group C (Frontend Pages):** Tasks 21, 22, 23, 24, 25 (independent pages)

Sequential dependencies:
- Task 1 → Task 2 → Tasks 3-6 → Task 7 → Tasks 8-9 → Task 10
- Task 12 → Task 13 → Tasks 14-16 → Tasks 17-20 → Tasks 21-25
- Task 11 (can run anytime)
