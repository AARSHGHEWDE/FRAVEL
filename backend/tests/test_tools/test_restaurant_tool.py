import pytest
import httpx
import respx

from app.tools.restaurant_tool import fetch_restaurants, FOURSQUARE_SEARCH_URL


@respx.mock
@pytest.mark.asyncio
async def test_fetch_restaurants_returns_options():
    respx.get(FOURSQUARE_SEARCH_URL).mock(
        return_value=httpx.Response(200, json={"results": [{
            "name": "Le Comptoir",
            "categories": [{"name": "French Restaurant"}],
            "rating": 9.0,
            "price": 3,
            "location": {"address": "123 Rue de Rivoli", "locality": "Paris", "country": "France"},
            "fsq_id": "abc123",
            "stats": {"total_ratings": 250},
        }]})
    )
    restaurants = await fetch_restaurants(location="Paris", api_key="test_key")
    assert len(restaurants) == 1
    assert restaurants[0].name == "Le Comptoir"
    assert restaurants[0].cuisine == "French Restaurant"
    assert restaurants[0].price_level == 3


@respx.mock
@pytest.mark.asyncio
async def test_fetch_restaurants_handles_api_error():
    respx.get(FOURSQUARE_SEARCH_URL).mock(
        return_value=httpx.Response(403, json={"message": "Forbidden"})
    )
    restaurants = await fetch_restaurants(location="Paris", api_key="bad_key")
    assert restaurants == []
