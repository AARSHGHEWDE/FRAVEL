from crewai import Agent, Task
from crewai.tools import BaseTool
import asyncio

from app.config import settings
from app.tools.restaurant_tool import fetch_restaurants


class RestaurantSearchTool(BaseTool):
    name: str = "search_restaurants"
    description: str = "Search for top restaurants in a city"
    location: str = ""

    def _run(self) -> str:
        restaurants = asyncio.run(fetch_restaurants(location=self.location, api_key=settings.foursquare_api_key))
        if not restaurants:
            return "No restaurants found."
        return "\n".join(
            f"- {r.name} ({r.cuisine}) - {r.rating}/5 {'$' * r.price_level} - {r.review_count} reviews"
            for r in restaurants
        )


def create_restaurant_agent(llm=None) -> Agent:
    return Agent(
        role="Restaurant Agent",
        goal="Find the best restaurants at the destination matching traveler preferences",
        backstory="You are a food critic and restaurant guide who knows the best dining options in every city, from street food to fine dining.",
        llm=llm, verbose=True,
    )


def create_restaurant_task(agent: Agent, city: str, interests: list[str], budget: float) -> Task:
    tool = RestaurantSearchTool(location=city)
    food_interests = [i for i in interests if i in ["food", "fine dining", "street food", "local cuisine"]]
    cuisine_hint = f" focusing on {', '.join(food_interests)}" if food_interests else ""
    return Task(
        description=f"Find the top 10 restaurants in {city}{cuisine_hint}. Budget is approximately ${budget} total for the trip. Include a mix of price ranges.",
        agent=agent, tools=[tool],
        expected_output="A list of top 10 restaurants with names, cuisines, ratings, and price levels.",
    )
