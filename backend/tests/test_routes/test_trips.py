import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_trip_returns_trip_id(client):
    with patch("app.routes.trips.PlannerService") as MockPlanner:
        instance = MockPlanner.return_value
        instance.plan = AsyncMock(return_value='{"title": "test"}')
        response = client.post("/api/trips", json={
            "origin": "New York", "destination": "Paris",
            "departure_date": "2026-06-15", "return_date": "2026-06-22",
            "budget": 3000.0, "interests": ["museums"], "travelers": 2,
        })
    assert response.status_code == 201
    data = response.json()
    assert "trip_id" in data
    assert data["status"] == "pending"


def test_create_trip_invalid_dates(client):
    response = client.post("/api/trips", json={
        "origin": "NYC", "destination": "Paris",
        "departure_date": "2026-06-22", "return_date": "2026-06-15",
    })
    assert response.status_code == 422
