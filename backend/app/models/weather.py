from datetime import date
from pydantic import BaseModel


class DayWeather(BaseModel):
    date: date
    temp_high_c: float
    temp_low_c: float
    condition: str
    icon: str
    humidity: int
    wind_speed_kmh: float
    precipitation_chance: int


class WeatherForecast(BaseModel):
    city: str
    days: list[DayWeather]
