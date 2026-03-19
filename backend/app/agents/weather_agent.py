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
        forecast = asyncio.run(fetch_weather(city=self.city, api_key=settings.openweather_api_key))
        if not forecast.days:
            return "Weather data unavailable."
        return "\n".join(
            f"- {d.date}: {d.condition}, {d.temp_low_c}-{d.temp_high_c}°C, rain {d.precipitation_chance}%, wind {d.wind_speed_kmh} km/h"
            for d in forecast.days
        )


def create_weather_agent(llm=None) -> Agent:
    return Agent(
        role="Weather Agent",
        goal="Provide accurate weather forecasts for trip planning",
        backstory="You are a meteorologist who provides clear, actionable weather forecasts to help travelers pack and plan activities.",
        llm=llm, verbose=True,
    )


def create_weather_task(agent: Agent, city: str) -> Task:
    tool = WeatherForecastTool(city=city)
    return Task(
        description=f"Get the weather forecast for {city}. Summarize conditions and recommend clothing/gear.",
        agent=agent, tools=[tool],
        expected_output="Day-by-day weather summary with packing recommendations.",
    )
