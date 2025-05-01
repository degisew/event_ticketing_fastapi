from typing import Any
import uuid

from sqlalchemy import select
from src.core.db import DbSession, atomic_transaction
from src.core.exceptions import (
    InternalInvariantError,
    NoEnoughTicketException,
    NotFoundException,
)
from src.core.models import DataLookup
from src.core.repositories import DataLookupRepository
from src.event.models.event import Ticket, TicketType
from src.event.models.reservation import Reservation
from src.event.schemas.reservation import ReservationResponseSchema, ReservationSchema
from src.event.enums import RESERVATION_STATUS_TYPE, ReservationStatuses, TicketStatuses


class ReservationService:
    @staticmethod
    def create_reservations(
        db: DbSession, validated_data: ReservationSchema
    ) -> ReservationResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(exclude_unset=True)

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

        with atomic_transaction(db):
            ReservationService.create_tickets(
                db, event_id, ticket_type_id, ticket_quantity
            )

            reservation = Reservation(
                **serialized_data,
                status=reservation_confirmed_status,
            )

            db.add(reservation)

            db.flush()

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
        event_id: uuid.UUID,
        ticket_type_id: uuid.UUID,
        ticket_quantity: int,
    ) -> list[Ticket]:
        ticket_status: DataLookup | None = db.scalar(
            select(DataLookup).where(
                DataLookup.type == TicketStatuses.TYPE.value,
                DataLookup.value == TicketStatuses.ACTIVE.value,
            )
        )
        if not ticket_status:
            raise InternalInvariantError("TicketStatuses.ACTIVE DataLookup not found.")
        # * trigger db row-locking using sqlalchemy with_for_update()
        # * to prevent race codition that leads to overbooking
        t_type: TicketType | None = db.execute(
            select(TicketType).where(TicketType.id == ticket_type_id).with_for_update()
        ).scalar_one_or_none()

        if not t_type:
            raise NotFoundException("Ticket type not found.")

        remaining_tickets: int = t_type.remaining_tickets
        if remaining_tickets < ticket_quantity:
            raise NoEnoughTicketException(
                f"No enough tickets available. Only {remaining_tickets} left."
            )

        tickets: list[Ticket] = [
            Ticket(
                event_id=event_id,
                status_id=ticket_status.id,
                ticket_type_id=ticket_type_id,
            )
            for _ in range(ticket_quantity)
        ]

        db.add_all(tickets)

        t_type.update_remaining_tickets(ticket_quantity)

        return tickets

    @staticmethod
    def get_reservations(db: DbSession) -> list[ReservationResponseSchema]:
        result = db.scalars(select(Reservation)).all()

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
