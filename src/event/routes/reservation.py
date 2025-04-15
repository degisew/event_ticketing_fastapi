from fastapi.routing import APIRouter

from src.core.db import DbSession

from src.event.schemas.reservation import ReservationSchema, ReservationResponseSchema
from src.event.services.reservation import ReservationService

router = APIRouter(prefix="/reservations")


@router.post("/")
async def create_reservations(
    db: DbSession, payload: ReservationSchema
) -> ReservationResponseSchema:
    return ReservationService.create_events(db, payload)
