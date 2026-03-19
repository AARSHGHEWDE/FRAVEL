import pytest
import httpx
import respx
from datetime import date

from app.tools.transport_tool import fetch_flights


@respx.mock
@pytest.mark.asyncio
async def test_fetch_flights_returns_options():
    respx.post("https://api.amadeus.com/v1/security/oauth2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok123", "expires_in": 1799})
    )
    respx.get("https://api.amadeus.com/v2/shopping/flight-offers").mock(
        return_value=httpx.Response(200, json={
            "data": [{
                "itineraries": [{
                    "duration": "PT12H0M",
                    "segments": [{
                        "carrierCode": "DL", "number": "123",
                        "departure": {"iataCode": "JFK", "at": "2026-06-15T08:00:00"},
                        "arrival": {"iataCode": "CDG", "at": "2026-06-15T20:00:00"},
                    }],
                }],
                "price": {"total": "850.00", "currency": "USD"},
                "travelerPricings": [{"fareDetailsBySegment": [{"cabin": "ECONOMY"}]}],
            }],
        })
    )
    flights = await fetch_flights(
        origin="JFK", destination="CDG", departure_date=date(2026, 6, 15),
        adults=1, api_key="key", api_secret="secret",
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
        origin="JFK", destination="CDG", departure_date=date(2026, 6, 15),
        adults=1, api_key="bad", api_secret="bad",
    )
    assert flights == []
