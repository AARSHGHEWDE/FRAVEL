from datetime import datetime
from pydantic import BaseModel


class FlightOption(BaseModel):
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    currency: str = "USD"
    stops: int = 0
    cabin_class: str = "economy"


class TrainOption(BaseModel):
    operator: str
    train_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    currency: str = "USD"
    class_type: str = "standard"
