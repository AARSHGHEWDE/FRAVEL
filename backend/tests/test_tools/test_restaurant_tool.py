import pytest
import httpx
import respx

from app.tools.restaurant_tool import fetch_restaurants


@respx.mock
@pytest.mark.asyncio
async def test_fetch_restaurants_returns_options():
    respx.get("https://api.yelp.com/v3/businesses/search").mock(
        return_value=httpx.Response(200, json={"businesses": [{
            "name": "Le Comptoir", "categories": [{"title": "French"}],
            "rating": 4.5, "price": "$$$",
            "location": {"display_address": ["123 Rue de Rivoli", "Paris"]},
            "phone": "+33123456789", "url": "https://yelp.com/biz/123",
            "image_url": "https://example.com/img.jpg", "review_count": 250,
        }]})
    )
    restaurants = await fetch_restaurants(location="Paris", api_key="test_key")
    assert len(restaurants) == 1
    assert restaurants[0].name == "Le Comptoir"
    assert restaurants[0].cuisine == "French"
    assert restaurants[0].price_level == 3


@respx.mock
@pytest.mark.asyncio
async def test_fetch_restaurants_handles_api_error():
    respx.get("https://api.yelp.com/v3/businesses/search").mock(
        return_value=httpx.Response(500, json={"error": {"code": "INTERNAL_ERROR"}})
    )
    restaurants = await fetch_restaurants(location="Paris", api_key="bad_key")
    assert restaurants == []
