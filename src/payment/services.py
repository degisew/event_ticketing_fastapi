from typing import Any
from sqlalchemy import ScalarResult
from src.core.db import DbSession, atomic_transaction
from src.core.exceptions import InternalInvariantError
from src.core.models import DataLookup
from src.core.repositories import DataLookupRepository
from src.event.repositories.ticket import TicketRepository
from src.payment.models import Transaction
from src.payment.repositories import TransactionRepository
from src.payment.schemas import PurchaseRequestSchema, PurchaseResponseSchema, TransactionResponseSchema
from src.event.enums import ReservationStatuses, TicketStatuses, RESERVATION_STATUS_TYPE


class PaymentService:
    @staticmethod
    def purchase_tickets(
        db: DbSession, payload: PurchaseRequestSchema
    ) -> PurchaseResponseSchema:

        serialized_data: dict[str, Any] = payload.model_dump(
            exclude_unset=True)
        reservation_id = serialized_data.get("reservation_id")

        reservation_status: DataLookup | None = DataLookupRepository.get_status_by_type(
            db, RESERVATION_STATUS_TYPE, ReservationStatuses.COMPLETED.value
        )

        if not reservation_status:
            raise InternalInvariantError(
                "ReservationStatuses.COMPLETED.value is missed in the DataLookup."
            )

        with atomic_transaction(db):
            instance: Transaction = TransactionRepository.create(
                db, serialized_data)

            instance.reservation.mark_as_completed(reservation_status)

            TicketRepository.update_ticket_by_reservation_id(
                db, reservation_id, TicketStatuses.SOLD.value
            )

            db.flush()

            db.refresh(instance)

        return PurchaseResponseSchema.model_validate(instance)

    @staticmethod
    def get_transactions(db: DbSession) -> list[TransactionResponseSchema]:
        transactions: ScalarResult[Transaction] = TransactionRepository.get_all_transactions(
            db)

        # TODO: Consider this might be an overhead for large transaction records
        return [TransactionResponseSchema.model_validate(trans) for trans in transactions]
