from uuid import UUID
from fastapi.routing import APIRouter
from src.account.dependencies import CurrentUser
from src.core.db import DbSession
from src.event.schemas.event import EventSchema, EventResponseSchema
from src.event.schemas.reservation import ReservationResponseSchema, ReservationSchema
from src.event.schemas.ticket import TicketTypeResponseSchema, TicketTypeSchema
from src.event.services.event import EventService
from src.event.services.reservation import ReservationService
from src.event.services.ticket_type import TicketTypeService

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


@router.post("/{event_id}/ticket_types")
async def create_ticket_types(
    db: DbSession, payload: TicketTypeSchema
) -> TicketTypeResponseSchema:
    return TicketTypeService.create_ticket_types(db, payload)


@router.get("/{event_id}/ticket_types")
async def get_ticket_types(
    db: DbSession,
    event_id
) -> list[TicketTypeResponseSchema]:
    return TicketTypeService.get_ticket_types(db, event_id)


@router.get("/{event_id}/ticket_types/{ticket_type_id}")
async def get_ticket_type(
    db: DbSession,
    event_id,
    ticket_type_id
) -> TicketTypeResponseSchema:
    return TicketTypeService.get_ticket_type(db, event_id,  ticket_type_id)


@router.patch("/{event_id}/ticket_types/{ticket_type_id}")
async def update_ticket_type(
    db: DbSession,
    ticket_type: TicketTypeResponseSchema,
    event_id,
    ticket_type_id
) -> TicketTypeResponseSchema:
    return TicketTypeService.update_ticket_type(db, ticket_type, event_id, ticket_type_id)


@router.post("/{event_id}/reservations")
async def create_reservations(
    db: DbSession,
    event_id: UUID,
    current_user: CurrentUser,
    payload: ReservationSchema
) -> ReservationResponseSchema:
    return ReservationService.create_reservations(db,  event_id, current_user, payload)


@router.get("/{event_id}/reservations")
async def get_Reservations(
    db: DbSession,
    event_id: UUID,
) -> list[ReservationResponseSchema]:
    return ReservationService.get_reservations(db, event_id)
