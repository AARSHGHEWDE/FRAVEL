import uuid

from fastapi import APIRouter, BackgroundTasks

from app.models.trip import TripRequest, TripResponse
from app.services.planner import PlannerService

router = APIRouter(prefix="/api/trips", tags=["trips"])

_trips: dict[str, dict] = {}
_planners: dict[str, PlannerService] = {}


@router.post("", status_code=201)
async def create_trip(trip: TripRequest, background_tasks: BackgroundTasks) -> TripResponse:
    trip_id = str(uuid.uuid4())
    planner = PlannerService(trip, trip_id)
    _trips[trip_id] = {"request": trip, "status": "pending"}
    _planners[trip_id] = planner
    background_tasks.add_task(planner.plan)
    return TripResponse(trip_id=trip_id, status="pending", request=trip)


@router.get("/{trip_id}")
async def get_trip(trip_id: str) -> TripResponse:
    trip_data = _trips.get(trip_id)
    if not trip_data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripResponse(
        trip_id=trip_id,
        status=trip_data["status"],
        request=trip_data["request"],
    )


def get_planner(trip_id: str) -> PlannerService | None:
    return _planners.get(trip_id)


@router.get("/{trip_id}/traces")
async def get_traces(trip_id: str) -> list[dict]:
    planner = _planners.get(trip_id)
    if not planner:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Trip not found")
    return planner.traces
