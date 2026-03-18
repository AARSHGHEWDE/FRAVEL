import pytest
from datetime import date, datetime


def test_trip_request_valid():
    from app.models.trip import TripRequest
    trip = TripRequest(
        origin="New York", destination="Paris",
        departure_date=date(2026, 6, 15), return_date=date(2026, 6, 22),
        budget=3000.0, interests=["museums", "food"], travelers=2,
    )
    assert trip.origin == "New York"
    assert trip.budget == 3000.0

def test_trip_request_return_after_departure():
    from app.models.trip import TripRequest
    with pytest.raises(ValueError):
        TripRequest(
            origin="NYC", destination="Paris",
            departure_date=date(2026, 6, 22), return_date=date(2026, 6, 15),
            budget=3000.0,
        )

def test_flight_option():
    from app.models.transport import FlightOption
    flight = FlightOption(
        airline="Delta", flight_number="DL123", origin="JFK", destination="CDG",
        departure_time=datetime(2026, 6, 15, 8, 0), arrival_time=datetime(2026, 6, 15, 20, 0),
        duration_minutes=720, price=850.0, currency="USD", stops=0, cabin_class="economy",
    )
    assert flight.airline == "Delta"
    assert flight.stops == 0

def test_event_option():
    from app.models.event import EventOption
    event = EventOption(
        name="Louvre Night Tour", venue="Louvre Museum",
        date=datetime(2026, 6, 16, 20, 0), category="museum",
        price=25.0, currency="USD", description="Evening tour of the Louvre",
        url="https://example.com", image_url="https://example.com/img.jpg",
    )
    assert event.name == "Louvre Night Tour"

def test_restaurant_option():
    from app.models.restaurant import RestaurantOption
    restaurant = RestaurantOption(
        name="Le Comptoir", cuisine="French", rating=4.5, price_level=3,
        address="123 Rue de Rivoli, Paris", phone="+33123456789",
        url="https://example.com", image_url="https://example.com/img.jpg",
        review_count=250,
    )
    assert restaurant.rating == 4.5
    assert restaurant.price_level == 3

def test_weather_forecast():
    from app.models.weather import DayWeather, WeatherForecast
    day = DayWeather(
        date=date(2026, 6, 15), temp_high_c=28.0, temp_low_c=18.0,
        condition="Sunny", icon="01d", humidity=45, wind_speed_kmh=12.0,
        precipitation_chance=10,
    )
    forecast = WeatherForecast(city="Paris", days=[day])
    assert forecast.city == "Paris"
    assert len(forecast.days) == 1

def test_itinerary():
    from app.models.itinerary import Activity, DayPlan, Itinerary
    activity = Activity(
        time="10:00", title="Visit Louvre", description="Explore the museum",
        category="sightseeing", cost=25.0, duration_minutes=180, location="Louvre Museum",
    )
    day = DayPlan(date=date(2026, 6, 16), title="Day 1 - Art & Culture", activities=[activity])
    itinerary = Itinerary(
        trip_id="abc123", title="Paris Adventure", days=[day],
        total_cost=2500.0, currency="USD",
    )
    assert itinerary.title == "Paris Adventure"
    assert len(itinerary.days) == 1
    assert len(itinerary.days[0].activities) == 1
