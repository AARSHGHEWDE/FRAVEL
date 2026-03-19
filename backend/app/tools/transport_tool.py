from datetime import date, datetime, timedelta

import httpx

from app.models.transport import FlightOption

AVIATIONSTACK_URL = "http://api.aviationstack.com/v1/flights"


async def fetch_flights(
    origin: str, destination: str, departure_date: date, adults: int,
    api_key: str, max_results: int = 10,
) -> list[FlightOption]:
    params = {
        "access_key": api_key,
        "dep_iata": origin,
        "arr_iata": destination,
        "flight_date": departure_date.isoformat(),
        "limit": max_results,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(AVIATIONSTACK_URL, params=params)
    if resp.status_code != 200:
        return []

    flights: list[FlightOption] = []
    for flight in resp.json().get("data", []):
        dep = flight.get("departure", {})
        arr = flight.get("arrival", {})
        airline = flight.get("airline", {}).get("iata", "??")
        flight_num = flight.get("flight", {}).get("iata", "??")

        dep_time_str = dep.get("scheduled")
        arr_time_str = arr.get("scheduled")
        if not dep_time_str or not arr_time_str:
            continue

        dep_time = datetime.fromisoformat(dep_time_str.replace("Z", "+00:00"))
        arr_time = datetime.fromisoformat(arr_time_str.replace("Z", "+00:00"))
        duration_minutes = int((arr_time - dep_time).total_seconds() / 60)

        flights.append(FlightOption(
            airline=airline,
            flight_number=flight_num,
            origin=dep.get("iata", origin),
            destination=arr.get("iata", destination),
            departure_time=dep_time,
            arrival_time=arr_time,
            duration_minutes=max(duration_minutes, 0),
            price=0.0,  # Aviationstack free tier doesn't include pricing
            currency="USD",
            stops=0,
            cabin_class="economy",
        ))
    return flights
