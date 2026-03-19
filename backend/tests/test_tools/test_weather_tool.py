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
                "dt": 1750003200,
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
