from pydantic import BaseModel, Field


class RestaurantOption(BaseModel):
    name: str
    cuisine: str
    rating: float = Field(ge=0, le=5)
    price_level: int = Field(ge=1, le=4)
    address: str
    phone: str = ""
    url: str = ""
    image_url: str = ""
    review_count: int = 0
