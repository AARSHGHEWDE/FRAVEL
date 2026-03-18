from datetime import date
from pydantic import BaseModel, model_validator


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: date
    budget: float = 5000.0
    interests: list[str] = []
    travelers: int = 1

    @model_validator(mode="after")
    def validate_dates(self):
        if self.return_date <= self.departure_date:
            raise ValueError("return_date must be after departure_date")
        return self


class TripResponse(BaseModel):
    trip_id: str
    status: str
    request: TripRequest
    itinerary_id: str | None = None
