from datetime import date, datetime
import re

import httpx

from app.models.transport import FlightOption

AMADEUS_AUTH_URL = "https://api.amadeus.com/v1/security/oauth2/token"
AMADEUS_FLIGHTS_URL = "https://api.amadeus.com/v2/shopping/flight-offers"


async def _get_amadeus_token(api_key: str, api_secret: str) -> str | None:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            AMADEUS_AUTH_URL,
            data={"grant_type": "client_credentials", "client_id": api_key, "client_secret": api_secret},
        )
    if resp.status_code != 200:
        return None
    return resp.json().get("access_token")


def _parse_duration(iso_duration: str) -> int:
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", iso_duration)
    if not match:
        return 0
    return int(match.group(1) or 0) * 60 + int(match.group(2) or 0)


async def fetch_flights(
    origin: str, destination: str, departure_date: date, adults: int,
    api_key: str, api_secret: str, max_results: int = 10,
) -> list[FlightOption]:
    token = await _get_amadeus_token(api_key, api_secret)
    if not token:
        return []

    params = {
        "originLocationCode": origin, "destinationLocationCode": destination,
        "departureDate": departure_date.isoformat(), "adults": adults,
        "max": max_results, "currencyCode": "USD",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            AMADEUS_FLIGHTS_URL, params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
    if resp.status_code != 200:
        return []

    flights: list[FlightOption] = []
    for offer in resp.json().get("data", []):
        itinerary = offer["itineraries"][0]
        segments = itinerary["segments"]
        first_seg, last_seg = segments[0], segments[-1]
        cabin = offer["travelerPricings"][0]["fareDetailsBySegment"][0].get("cabin", "ECONOMY")
        flights.append(FlightOption(
            airline=first_seg["carrierCode"],
            flight_number=f"{first_seg['carrierCode']}{first_seg['number']}",
            origin=first_seg["departure"]["iataCode"],
            destination=last_seg["arrival"]["iataCode"],
            departure_time=datetime.fromisoformat(first_seg["departure"]["at"]),
            arrival_time=datetime.fromisoformat(last_seg["arrival"]["at"]),
            duration_minutes=_parse_duration(itinerary["duration"]),
            price=float(offer["price"]["total"]),
            currency=offer["price"].get("currency", "USD"),
            stops=len(segments) - 1,
            cabin_class=cabin.lower(),
        ))
    return flights
