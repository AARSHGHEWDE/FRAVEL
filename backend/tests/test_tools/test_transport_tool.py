import pytest
import httpx
import respx
from datetime import date

from app.tools.transport_tool import fetch_flights, AVIATIONSTACK_URL


@respx.mock
@pytest.mark.asyncio
async def test_fetch_flights_returns_options():
    respx.get(AVIATIONSTACK_URL).mock(
        return_value=httpx.Response(200, json={
            "data": [{
                "airline": {"iata": "DL"},
                "flight": {"iata": "DL123"},
                "departure": {"iata": "JFK", "scheduled": "2026-06-15T08:00:00+00:00"},
                "arrival": {"iata": "CDG", "scheduled": "2026-06-15T20:00:00+00:00"},
            }],
        })
    )
    flights = await fetch_flights(
        origin="JFK", destination="CDG", departure_date=date(2026, 6, 15),
        adults=1, api_key="test_key",
    )
    assert len(flights) == 1
    assert flights[0].airline == "DL"
    assert flights[0].flight_number == "DL123"
    assert flights[0].duration_minutes == 720


@respx.mock
@pytest.mark.asyncio
async def test_fetch_flights_handles_api_error():
    respx.get(AVIATIONSTACK_URL).mock(
        return_value=httpx.Response(401, json={"error": {"code": "invalid_access_key"}})
    )
    flights = await fetch_flights(
        origin="JFK", destination="CDG", departure_date=date(2026, 6, 15),
        adults=1, api_key="bad",
    )
    assert flights == []
