import asyncio
import uuid
from collections.abc import AsyncGenerator

from app.models.trip import TripRequest
from app.agents.crew import build_crew
from app.services.supabase_client import get_supabase


class PlannerService:
    """Orchestrates the CrewAI crew and streams status via SSE."""

    def __init__(self, trip_request: TripRequest, trip_id: str | None = None):
        self.trip = trip_request
        self.trip_id = trip_id or str(uuid.uuid4())
        self._status_queue: asyncio.Queue[dict] = asyncio.Queue()

    async def _emit(self, agent: str, status: str, detail: str = ""):
        await self._status_queue.put({"agent": agent, "status": status, "detail": detail})

    async def stream_status(self) -> AsyncGenerator[dict, None]:
        """Yield SSE events as the crew works."""
        while True:
            event = await self._status_queue.get()
            yield event
            if event.get("status") == "complete" and event.get("agent") == "system":
                break

    async def plan(self) -> str:
        """Run the crew and return the itinerary JSON."""
        crew = build_crew(self.trip)
        await self._emit("system", "started", "Planning your trip...")

        agent_names = ["Transport Agent", "Events Agent", "Restaurant Agent", "Weather Agent", "Itinerary Compiler"]
        for name in agent_names:
            await self._emit(name, "working", f"{name} is researching...")

        result = await asyncio.to_thread(crew.kickoff)

        for name in agent_names:
            await self._emit(name, "done")

        try:
            db = get_supabase()
            db.table("trips").upsert({
                "id": self.trip_id,
                "request": self.trip.model_dump(mode="json"),
                "result": str(result),
                "status": "complete",
            }).execute()
        except Exception:
            pass  # Don't fail if DB is unavailable

        await self._emit("system", "complete", str(result))
        return str(result)
