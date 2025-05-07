from fastapi.routing import APIRouter

from src.core.db import DbSession
from src.payment.schemas import (
    PurchaseRequestSchema,
    PurchaseResponseSchema,
    TransactionResponseSchema
)
from src.payment.services import PaymentService

router = APIRouter(prefix="/payments")


@router.post("/")
async def purchase_tickets(
    db: DbSession, payload: PurchaseRequestSchema
) -> PurchaseResponseSchema:

    return PaymentService.purchase_tickets(db, payload)


@router.get("/")
async def get_transactions(db: DbSession) -> list[TransactionResponseSchema]:
    return PaymentService.get_transactions(db)
