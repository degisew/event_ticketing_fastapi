import uuid
from typing import Any
from sqlalchemy import ScalarResult
from src.core.db import DbSession, atomic_transaction
from src.core.exceptions import InternalInvariantError
from src.core.models import DataLookup
from src.core.repositories import DataLookupRepository
from src.event.repositories.ticket import TicketRepository
from src.payment.models import Transaction
from src.payment.repositories import TransactionRepository
from src.payment.schemas import (
    PurchaseRequestSchema,
    PurchaseResponseSchema,
    TransactionResponseSchema
)
from src.event.enums import (
    TICKET_STATUS_TYPE,
    RESERVATION_STATUS_TYPE,
    ReservationStatuses,
    TicketStatuses,
)
from src.payment.enums import (
    TRANSACTION_PAYMENT_STATUS_TYPE,
    TransactionPaymentStatuses
)


class PaymentService:
    @staticmethod
    def purchase_tickets(
        db: DbSession, payload: PurchaseRequestSchema
    ) -> PurchaseResponseSchema:

        serialized_data: dict[str, Any] = payload.model_dump(
            exclude_unset=True)

        reservation_id: uuid.UUID | None = serialized_data.get(
            "reservation_id")
        payment_status: DataLookup | None = DataLookupRepository.get_status_by_type(
            db,
            TRANSACTION_PAYMENT_STATUS_TYPE,
            TransactionPaymentStatuses.COMPLETED.value
        )

        if not payment_status:
            raise InternalInvariantError(
                "TransactionPaymentStatuses.COMPLETED.value is missed in the DataLookup."
            )

        serialized_data["payment_status"] = payment_status

        reservation_status: DataLookup | None = DataLookupRepository.get_status_by_type(
            db,
            RESERVATION_STATUS_TYPE,
            ReservationStatuses.COMPLETED.value
        )

        if not reservation_status:
            raise InternalInvariantError(
                "ReservationStatuses.COMPLETED is missed in the DataLookup."
            )

        sold_ticket_status: DataLookup | None = DataLookupRepository.get_status_by_type(
            db,
            TICKET_STATUS_TYPE,
            TicketStatuses.SOLD.value
        )
        if not sold_ticket_status:
            raise InternalInvariantError(
                "TicketStatuses.SOLD is missed in the DataLookup.")

        with atomic_transaction(db):
            instance: Transaction = TransactionRepository.create(
                db, serialized_data)

            db.flush()

            instance.reservation.mark_as_completed(reservation_status)

            TicketRepository.update_ticket_by_reservation_id(
                db,
                reservation_id,
                sold_ticket_status.id
            )

            db.refresh(instance)

        return PurchaseResponseSchema.model_validate(instance)

    @staticmethod
    def get_transactions(db: DbSession) -> list[TransactionResponseSchema]:
        transactions = TransactionRepository.get_all_transactions(db)

        # TODO: Consider this might be an overhead for large transaction records
        return [TransactionResponseSchema.model_validate(trans) for trans in transactions]
