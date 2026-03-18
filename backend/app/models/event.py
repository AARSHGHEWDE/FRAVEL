from datetime import datetime
from pydantic import BaseModel


class EventOption(BaseModel):
    name: str
    venue: str
    date: datetime
    category: str
    price: float | None = None
    currency: str = "USD"
    description: str = ""
    url: str = ""
    image_url: str = ""
