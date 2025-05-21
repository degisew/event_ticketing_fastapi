from uuid import UUID
from fastapi import BackgroundTasks
from fastapi.routing import APIRouter

from src.account.dependencies import CurrentUser
from src.core.db import DbSession

from src.event.background_tasks import send_email
from src.event.schemas.reservation import ReservationResponseSchema
from src.event.services.reservation import ReservationService
from src.event.schemas.reservation import (
    PurchaseRequestSchema,
    PurchaseResponseSchema
)

router = APIRouter(prefix="/reservations")


@router.get("/me")
async def get_my_reservations(
    db: DbSession,
    current_user: CurrentUser
) -> list[ReservationResponseSchema]:
    return ReservationService.get_user_reservations(db, current_user)


@router.post("/{reservation_id}/payments")
async def purchase_tickets(
    db: DbSession,
    current_user: CurrentUser,
    reservation_id: UUID,
    payload: PurchaseRequestSchema,
    bg_tasks: BackgroundTasks
) -> PurchaseResponseSchema:
    response = ReservationService.purchase_tickets(
        db, current_user, reservation_id, payload)

    # TODO: We may need to remove user_id here if
    # TODO: we're going to receive User obj from the payload
    bg_tasks.add_task(
        send_email,
        user_id=response.user_id,
        reservation_id=response.reservation_id
    )

    return response
