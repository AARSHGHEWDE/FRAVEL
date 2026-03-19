import httpx

from app.models.restaurant import RestaurantOption

FOURSQUARE_SEARCH_URL = "https://api.foursquare.com/v3/places/search"


async def fetch_restaurants(
    location: str, api_key: str, cuisine: str | None = None, max_results: int = 20,
) -> list[RestaurantOption]:
    params: dict = {
        "near": location,
        "categories": "13000",  # Foursquare category ID for Food
        "limit": max_results,
        "sort": "RATING",
    }
    if cuisine:
        params["query"] = cuisine

    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(FOURSQUARE_SEARCH_URL, params=params, headers=headers)
    if resp.status_code != 200:
        return []

    restaurants: list[RestaurantOption] = []
    for place in resp.json().get("results", []):
        categories = place.get("categories", [])
        cuisine_name = categories[0].get("name", "Restaurant") if categories else "Restaurant"
        location_data = place.get("location", {})
        address_parts = [
            location_data.get("address", ""),
            location_data.get("locality", ""),
            location_data.get("country", ""),
        ]
        address = ", ".join(p for p in address_parts if p)

        restaurants.append(RestaurantOption(
            name=place.get("name", ""),
            cuisine=cuisine_name,
            rating=round(place.get("rating", 7.0) / 2, 1),  # Foursquare rates 0-10, convert to 0-5
            price_level=place.get("price", 2),  # Foursquare 1-4
            address=address,
            phone="",
            url=f"https://foursquare.com/v/{place.get('fsq_id', '')}",
            image_url="",
            review_count=place.get("stats", {}).get("total_ratings", 0),
        ))
    return restaurants
