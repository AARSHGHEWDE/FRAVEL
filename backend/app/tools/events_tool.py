from datetime import date, datetime

import httpx

from app.models.event import EventOption

TICKETMASTER_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


async def fetch_events(
    city: str, start_date: date, end_date: date, api_key: str, max_results: int = 20,
) -> list[EventOption]:
    params = {
        "apikey": api_key, "city": city,
        "startDateTime": f"{start_date.isoformat()}T00:00:00Z",
        "endDateTime": f"{end_date.isoformat()}T23:59:59Z",
        "size": max_results, "sort": "relevance,desc",
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
        events.append(EventOption(
            name=raw.get("name", ""), venue=venue_name, date=event_date,
            category=category, price=price, currency=currency,
            description=raw.get("info", ""), url=raw.get("url", ""), image_url=image_url,
        ))
    return events
