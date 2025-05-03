import uuid
from typing import Any
from src.core.db import DbSession, atomic_transaction
from src.core.exceptions import (
    InternalInvariantError,
    NoEnoughTicketException,
    NotFoundException,
)
from src.core.models import DataLookup
from src.core.repositories import DataLookupRepository
from src.event.models.event import Ticket, TicketType
from src.event.repositories.event import TicketTypeRepository
from src.event.repositories.reservation import ReservationRepository
from src.event.repositories.ticket import TicketRepository
from src.event.schemas.reservation import (
    ReservationResponseSchema,
    ReservationSchema
)
from src.event.enums import (
    RESERVATION_STATUS_TYPE,
    TICKET_STATUS_TYPE,
    ReservationStatuses,
    TicketStatuses
)


class ReservationService:
    @staticmethod
    def create_reservations(
        db: DbSession, validated_data: ReservationSchema
    ) -> ReservationResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True)

        ticket_type_id = serialized_data.get("ticket_type_id")
        event_id = serialized_data.get("event_id")
        ticket_quantity = serialized_data.get("ticket_quantity")

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
            reservation = ReservationRepository.create(db, serialized_data)

            ReservationService.create_tickets(
                db, reservation.id, event_id, ticket_type_id, ticket_quantity
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
            ticket_type_id=ticket_type_id,
            locking_needed=True  # db level row-locking to avoid race condition.
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
    def get_reservations(db: DbSession) -> list[ReservationResponseSchema]:
        result = ReservationRepository.get_reservations(db)

        return [ReservationResponseSchema.model_validate(res) for res in result]

    # @staticmethod
    # def get_reservation(
    #     db: DbSession, reservation_id: uuid.UUID
    # ) -> ReservationResponseSchema:
    #     pass

    # @staticmethod
    # def update_reservation(
    #     db: DbSession,reservation_id: uuid.UUID, reservation: ReservationSchema
    # ) -> ReservationResponseSchema:
    #     pass
