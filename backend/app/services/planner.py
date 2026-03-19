import asyncio
import time
import uuid
from collections.abc import AsyncGenerator

from app.models.trip import TripRequest
from app.agents.crew import build_crew
from app.services.supabase_client import get_supabase

AGENT_ORDER = [
    "Transport Agent",
    "Events Agent",
    "Restaurant Agent",
    "Weather Agent",
    "Itinerary Compiler",
]


class PlannerService:
    """Orchestrates the CrewAI crew and streams status via SSE."""

    def __init__(self, trip_request: TripRequest, trip_id: str | None = None):
        self.trip = trip_request
        self.trip_id = trip_id or str(uuid.uuid4())
        self._status_queue: asyncio.Queue[dict] = asyncio.Queue()
        self.traces: list[dict] = []

    async def _emit(self, agent: str, status: str, detail: str = "") -> None:
        await self._status_queue.put({"agent": agent, "status": status, "detail": detail})

    def _emit_threadsafe(self, loop: asyncio.AbstractEventLoop, agent: str, status: str, detail: str = "") -> None:
        loop.call_soon_threadsafe(
            self._status_queue.put_nowait,
            {"agent": agent, "status": status, "detail": detail},
        )

    async def stream_status(self) -> AsyncGenerator[dict, None]:
        """Yield SSE events as the crew works."""
        while True:
            event = await self._status_queue.get()
            yield event
            if event.get("status") == "complete" and event.get("agent") == "system":
                break

    async def plan(self) -> str:
        """Run the crew and return the itinerary JSON."""
        loop = asyncio.get_event_loop()
        completed_count = 0
        task_start_times: dict[str, float] = {}

        def task_callback(output: object) -> None:
            nonlocal completed_count
            # Determine which agent just finished
            agent_name = AGENT_ORDER[completed_count] if completed_count < len(AGENT_ORDER) else "Unknown"

            # Get raw output string
            raw = getattr(output, "raw", None) or str(output)
            task_desc = getattr(output, "description", "") or ""

            # Store trace
            duration = round(time.time() - task_start_times.get(agent_name, time.time()), 1)
            self.traces.append({
                "agent": agent_name,
                "task": task_desc[:300] if task_desc else f"{agent_name} task",
                "output": raw,
                "duration_seconds": duration,
                "completed_at": time.strftime("%H:%M:%S"),
            })

            # Mark current agent done
            self._emit_threadsafe(loop, agent_name, "done", "")
            completed_count += 1

            # Emit next agent as working
            if completed_count < len(AGENT_ORDER):
                next_agent = AGENT_ORDER[completed_count]
                task_start_times[next_agent] = time.time()
                self._emit_threadsafe(loop, next_agent, "working", f"{next_agent} is researching...")

        crew = build_crew(self.trip, task_callback=task_callback)
        await self._emit("system", "started", "Planning your trip...")

        # Kick off first agent immediately
        task_start_times[AGENT_ORDER[0]] = time.time()
        await self._emit(AGENT_ORDER[0], "working", f"{AGENT_ORDER[0]} is researching...")

        result = await asyncio.to_thread(crew.kickoff)

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
