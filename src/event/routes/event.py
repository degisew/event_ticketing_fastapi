from fastapi.routing import APIRouter
from src.core.db import DbSession
from src.event.schemas.event import EventSchema, EventResponseSchema
from src.event.services.event import EventService

router = APIRouter(prefix="/events")


@router.post("/")
async def create_events(db: DbSession, payload: EventSchema) -> EventResponseSchema:
    return EventService.create_events(db, payload)


@router.get("/")
async def get_events(db: DbSession) -> list[EventResponseSchema]:
    return EventService.get_events(db)


@router.get("/{event_id}")
async def get_event(db: DbSession, event_id) -> EventResponseSchema:
    return EventService.get_event(db, event_id)


@router.patch("/{event_id}")
async def update_event(
    db: DbSession, event: EventSchema, event_id
) -> EventResponseSchema:
    return EventService.update_event(db, event, event_id)

