import json

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.routes.trips import get_planner

router = APIRouter(prefix="/api/trips", tags=["sse"])


@router.get("/{trip_id}/stream")
async def stream_trip_status(trip_id: str):
    planner = get_planner(trip_id)
    if not planner:
        raise HTTPException(status_code=404, detail="Trip not found")

    async def event_generator():
        async for event in planner.stream_status():
            yield {"event": "agent_status", "data": json.dumps(event)}

    return EventSourceResponse(event_generator())
