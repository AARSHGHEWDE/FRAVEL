import httpx

from app.models.restaurant import RestaurantOption

YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"


def _price_to_level(price_str: str) -> int:
    return len(price_str) if price_str else 2


async def fetch_restaurants(
    location: str, api_key: str, cuisine: str | None = None, max_results: int = 20,
) -> list[RestaurantOption]:
    params: dict = {
        "location": location,
        "term": f"{cuisine} restaurants" if cuisine else "restaurants",
        "sort_by": "rating", "limit": max_results,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(YELP_SEARCH_URL, params=params, headers=headers)
    if resp.status_code != 200:
        return []

    restaurants: list[RestaurantOption] = []
    for biz in resp.json().get("businesses", []):
        categories = biz.get("categories", [])
        cuisine_name = categories[0].get("title", "Unknown") if categories else "Unknown"
        address_parts = biz.get("location", {}).get("display_address", [])
        restaurants.append(RestaurantOption(
            name=biz.get("name", ""), cuisine=cuisine_name,
            rating=biz.get("rating", 0),
            price_level=_price_to_level(biz.get("price", "$$")),
            address=", ".join(address_parts),
            phone=biz.get("phone", ""), url=biz.get("url", ""),
            image_url=biz.get("image_url", ""),
            review_count=biz.get("review_count", 0),
        ))
    return restaurants
