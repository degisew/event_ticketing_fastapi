# from fastapi.routing import APIRouter
# from src.core.db import DbSession
# from src.event.schemas.reservation import TransactionResponseSchema
# from src.payment.services import PaymentService


# router = APIRouter()


# @router.post("/reservations/{reservation_id}/payments")
# async def purchase_tickets(
#     db: DbSession,
#     current_user: CurrentUser,
#     reservation_id: UUID,
#     payload: PurchaseRequestSchema,
#     bg_tasks: BackgroundTasks
# ) -> PurchaseResponseSchema:
#     response = PaymentService.purchase_tickets(db, current_user, reservation_id, payload)

#     # TODO: We may need to remove user_id here if
#     # TODO: we're going to receive User obj from the payload
#     bg_tasks.add_task(
#         send_email,
#         user_id=response.user_id,
#         reservation_id=response.reservation_id
#     )

#     return response


# @router.get("/payments")
# async def get_transactions(
#     db: DbSession,
# ) -> list[TransactionResponseSchema]:
#     return PaymentService.get_transactions(db)
