from fastapi.routing import APIRouter
from fastapi import BackgroundTasks, Response
from src.core.db import DbSession
from src.payment.schemas import (
    PurchaseRequestSchema,
    PurchaseResponseSchema,
    TransactionResponseSchema
)
from src.payment.services import PaymentService
from src.event.background_tasks import send_email


router = APIRouter(prefix="/payments")


@router.post("/")
async def purchase_tickets(
    db: DbSession,
    payload: PurchaseRequestSchema,
    bg_tasks: BackgroundTasks
) -> PurchaseResponseSchema:
    response = PaymentService.purchase_tickets(db, payload)

    # TODO: We may need to remove user_id here if
    # TODO: we're going to receive User obj from the payload
    bg_tasks.add_task(
        send_email,
        user_id=response.user_id,
        reservation_id=response.reservation_id
    )

    return response


@router.get("/")
async def get_transactions(db: DbSession) -> list[TransactionResponseSchema]:
    return PaymentService.get_transactions(db)
