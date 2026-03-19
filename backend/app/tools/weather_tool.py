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
