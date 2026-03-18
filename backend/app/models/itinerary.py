from datetime import date
from pydantic import BaseModel

from app.models.weather import DayWeather


class Activity(BaseModel):
    time: str
    title: str
    description: str
    category: str
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
