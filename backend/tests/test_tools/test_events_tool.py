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
            "_embedded": {"events": [{
                "name": "Jazz Festival",
                "_embedded": {"venues": [{"name": "Olympia Hall"}]},
                "dates": {"start": {"dateTime": "2026-06-16T20:00:00Z"}},
                "classifications": [{"segment": {"name": "Music"}}],
                "priceRanges": [{"min": 50.0, "currency": "USD"}],
                "info": "A night of jazz",
                "url": "https://example.com/event",
                "images": [{"url": "https://example.com/img.jpg"}],
            }]}
        })
    )
    events = await fetch_events(city="Paris", start_date=date(2026, 6, 15), end_date=date(2026, 6, 22), api_key="test_key")
    assert len(events) == 1
    assert events[0].name == "Jazz Festival"
    assert events[0].venue == "Olympia Hall"


@respx.mock
@pytest.mark.asyncio
async def test_fetch_events_handles_no_results():
    respx.get("https://app.ticketmaster.com/discovery/v2/events.json").mock(
        return_value=httpx.Response(200, json={})
    )
    events = await fetch_events(city="Nowhere", start_date=date(2026, 6, 15), end_date=date(2026, 6, 22), api_key="test_key")
    assert events == []
