from decimal import Decimal
import uuid
from typing import Any
from src.account.dependencies import CurrentUser
from src.core.db import DbSession, atomic_transaction
from src.core.exceptions import (
    InternalInvariantError,
    NoEnoughTicketException,
    NotFoundException,
)
from src.core.models import DataLookup
from src.core.repositories import DataLookupRepository
from src.event.models.event import Ticket, TicketType
from src.event.models.reservation import Reservation, Transaction
from src.event.repositories.event import TicketTypeRepository
from src.event.repositories.reservation import ReservationRepository
from src.event.repositories.ticket import TicketRepository
from src.event.repositories.transaction import TransactionRepository
from src.event.schemas.reservation import (
    CheckoutSummaryResponseSchema,
    PurchaseRequestSchema,
    PurchaseResponseSchema,
    ReservationResponseSchema,
    ReservationSchema,
    TransactionResponseSchema
)
from src.event.enums import (
    RESERVATION_STATUS_TYPE,
    TICKET_STATUS_TYPE,
    TRANSACTION_PAYMENT_STATUS_TYPE,
    ReservationStatuses,
    TicketStatuses,
    TransactionPaymentStatuses
)


class ReservationService:
    @staticmethod
    def create_reservations(
        db: DbSession,
        event_id: uuid.UUID,
        current_user: CurrentUser,
        validated_data: ReservationSchema
    ) -> ReservationResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True)

        serialized_data["event_id"] = event_id
        serialized_data["user_id"] = current_user.id
        ticket_type_id = serialized_data.get("ticket_type_id")
        ticket_quantity = serialized_data.get("ticket_quantity")

        # VALIDATION of the ticket type belongs to event
        ticket_type: TicketType | None = TicketTypeRepository.get_ticket_type(
            db, event_id, ticket_type_id)

        if not ticket_type:
            raise NotFoundException("Valid ticket type not found.")

        reservation_confirmed_status: DataLookup | None = (
            DataLookupRepository.get_status_by_type(
                db,
                RESERVATION_STATUS_TYPE,
                ReservationStatuses.CONFIRMED.value,
            )
        )

        if not reservation_confirmed_status:
            raise InternalInvariantError(
                "ReservationStatuses.CONFIRMED DataLookup not found."
            )

        serialized_data["status"] = reservation_confirmed_status

        with atomic_transaction(db):
            reservation = ReservationRepository.create(
                db,
                serialized_data
            )

            ReservationService.create_tickets(
                db,
                reservation.id,
                event_id,
                ticket_type_id,
                ticket_quantity
            )

            db.refresh(reservation)

        return ReservationResponseSchema.model_validate(reservation)

        # @staticmethod
        # def assign_seats(
        #     db: DbSession,
        #     event_id: uuid.UUID,
        #     ticket_type_id: uuid.UUID,
        #     ticket_quantity: int,
        # ) -> Sequence[Seat]:
        #     try:
        #         seat_available_status: DataLookup | None = db.scalar(
        #             select(DataLookup).where(
        #                 DataLookup.type == SeatStatuses.TYPE.value,
        #                 DataLookup.value == SeatStatuses.AVAILABLE.value,
        #             )
        #         )

        #         seat_reserved_status: DataLookup | None = db.scalar(
        #             select(DataLookup).where(
        #                 DataLookup.type == SeatStatuses.TYPE.value,
        #                 DataLookup.value == SeatStatuses.RESERVED.value,
        #             )
        #         )

        #         if not seat_available_status:
        #             raise InternalInvariantError(
        #                 "SeatStatuses.AVAILABLE DataLookup not found."
        #             )

        #         if not seat_reserved_status:
        #             raise InternalInvariantError(
        #                 "SeatStatuses.RESERVED DataLookup not found."
        #             )

        #         seats: Sequence[Seat] = db.scalars(
        #             select(Seat)
        #             .where(
        #                 Seat.event_id == event_id,
        #                 Seat.status_id == seat_available_status
        #             )
        #             .order_by(Seat.section)
        #             .limit(ticket_quantity)
        #         ).all()

        #         if len(seats) < ticket_quantity:
        #             raise ValueError("No Enough available seats.")

        #         for seat in seats:
        #             seat.status = seat_reserved_status

        #         return seats

        #     except Exception as e:
        #         raise e

    @staticmethod
    def create_tickets(
        db: DbSession,
        reservation_id: uuid.UUID,
        event_id: uuid.UUID,
        ticket_type_id: uuid.UUID,
        ticket_quantity: int,
    ) -> list[Ticket]:
        ticket_status: DataLookup | None = DataLookupRepository.get_status_by_type(
            db,
            TICKET_STATUS_TYPE,
            TicketStatuses.ACTIVE.value,
        )
        if not ticket_status:
            raise InternalInvariantError(
                "TicketStatuses.ACTIVE DataLookup not found.")

        t_type: TicketType | None = TicketTypeRepository.get_ticket_type(
            db=db,
            event_id=event_id,
            ticket_type_id=ticket_type_id,
            # db level row-locking to avoid race condition.
            locking_needed=True
        )

        if not t_type:
            raise NotFoundException("Ticket type not found.")

        remaining_tickets: int = t_type.remaining_tickets

        if remaining_tickets < ticket_quantity:
            raise NoEnoughTicketException(
                f"No enough tickets available. Only {remaining_tickets} left."
            )

        tickets: list[Ticket] = TicketRepository.create(
            db,
            event_id,
            reservation_id,
            ticket_quantity,
            ticket_status.id,
            ticket_type_id
        )

        t_type.update_remaining_tickets(ticket_quantity)

        return tickets

    @staticmethod
    def get_reservations(
        db: DbSession,
        event_id: uuid.UUID,
    ) -> list[ReservationResponseSchema]:
        result = ReservationRepository.get_reservations(db, event_id)

        return [ReservationResponseSchema.model_validate(res) for res in result]

    @staticmethod
    def get_user_reservations(
        db: DbSession,
        current_user: CurrentUser
    ):
        result = ReservationRepository.get_reservations_by_user(
            db,
            current_user.id
        )

        return [ReservationResponseSchema.model_validate(res) for res in result]

    @staticmethod
    def calculate_total_payment(
        db: DbSession,
        reservation_id: uuid.UUID
    ) -> CheckoutSummaryResponseSchema:
        reservation: Reservation | None = ReservationRepository.get_reservation_by_id(
            db,
            reservation_id
        )
        if not reservation:
            raise NotFoundException("Reservation not found.")

        ticket_type: TicketType = reservation.ticket_type
        quantity: int = reservation.ticket_quantity
        unit_price: Decimal = ticket_type.price
        total_price: Decimal = unit_price * quantity

        return CheckoutSummaryResponseSchema(
            reservation_id=reservation_id,
            ticket_type=ticket_type.name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )

    @staticmethod
    def purchase_tickets(
        db: DbSession,
        current_user: CurrentUser,
        reservation_id: uuid.UUID,
        payload: PurchaseRequestSchema
    ) -> PurchaseResponseSchema:

        serialized_data: dict[str, Any] = payload.model_dump(
            exclude_unset=True)

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

        serialized_data["user_id"] = current_user.id

        serialized_data["reservation_id"] = reservation_id

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
    def get_transactions(
        db: DbSession,
    ) -> list[TransactionResponseSchema]:
        transactions = TransactionRepository.get_all_transactions(db)

        # TODO: Consider this might be an overhead for large transaction records
        return [TransactionResponseSchema.model_validate(trans) for trans in transactions]
