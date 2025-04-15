from typing import Any, Sequence
import uuid

from sqlalchemy import select
from src.core.db import DbSession
from src.core.exceptions import InternalInvariantError
from src.core.models import DataLookup
from src.event.models.event import Seat, Ticket
from src.event.models.reservation import Reservation
from src.event.schemas.reservation import ReservationResponseSchema, ReservationSchema
from src.event.enums import SeatStatuses, TicketStatuses


class ReservationService:
    @staticmethod
    def create_reservations(
        db: DbSession, validated_data: ReservationSchema
    ) -> ReservationResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(exclude_unset=True)

        ticket_type_id = serialized_data.get("ticket_type_id")

        event_id = serialized_data.get("event_id")

        ticket_quantity = serialized_data.get("ticket_quantity")

        tickets: list[Ticket] = ReservationService.create_tickets(
            db, event_id, ticket_type_id, ticket_quantity
        )

        reservation = Reservation(
            **serialized_data,
            status=reservation_booked_status
            user_id=current_logged_in_user,
            
        )

        db.add(reservation)

        db.commit()

        db.refresh(reservation)

        return ReservationResponseSchema.model_validate(reservation)


    @staticmethod
    def assign_seats(
        db: DbSession,
        event_id: uuid.UUID,
        ticket_type_id: uuid.UUID,
        ticket_quantity: int,
    ) -> Sequence[Seat]:
        # TODO: Find a way to get the consecutive available seats
        # TODO: based on the user's ticket type choice
        try:
            seat_available_status: DataLookup | None = db.scalar(
                select(DataLookup).where(
                    DataLookup.type == SeatStatuses.TYPE.value,
                    DataLookup.value == SeatStatuses.AVAILABLE.value,
                )
            )

            seat_reserved_status: DataLookup | None = db.scalar(
                select(DataLookup).where(
                    DataLookup.type == SeatStatuses.TYPE.value,
                    DataLookup.value == SeatStatuses.RESERVED.value,
                )
            )

            if not seat_available_status:
                raise InternalInvariantError(
                    "TicketStatuses.ACTIVE DataLookup not found."
                )

            if not seat_reserved_status:
                raise InternalInvariantError(
                    "TicketStatuses.RESERVED DataLookup not found."
                )

            seats: Sequence[Seat] = db.scalars(
                select(Seat).where(
                    Seat.event_id == event_id,
                    Seat.status_id == seat_available_status
                )
                .order_by(Seat.section)
                .limit(ticket_quantity)
            ).all()

            if len(seats) < ticket_quantity:
                raise ValueError("No Enough available seats.")

            for seat in seats:
                seat.status = seat_reserved_status

            return seats

        except Exception as e:
            raise e

    @staticmethod
    def create_tickets(
        db: DbSession, event_id, ticket_type_id, ticket_quantity
    ) -> list[Ticket]:
        try:
            ticket_status = db.scalar(
                select(DataLookup).where(
                    DataLookup.type == TicketStatuses.TYPE.value,
                    DataLookup.value == TicketStatuses.ACTIVE.value,
                )
            )
            if not ticket_status:
                raise InternalInvariantError(
                    "Expected TicketStatuses.ACTIVE in DataLookup but not found."
                )
            seats: Sequence[Seat] = ReservationService.assign_seats(
                db,
                event_id,
                ticket_type_id,
                ticket_quantity
            )

            tickets: list[Ticket] = []

            for seat in seats:
                instance = Ticket(
                    event_id=event_id,
                    status=ticket_status,
                    ticket_type_id=ticket_type_id,
                    seat_id=seat.id,
                )

                db.add(instance)

                tickets.append(instance)

            instance.ticket_type.update_remaining_tickets(ticket_quantity)

            db.commit()

            return tickets

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_reservations(db: DbSession) -> list[ReservationResponseSchema]:
        pass

    @staticmethod
    def get_reservation(
        db: DbSession, reservation_id: uuid.UUID
    ) -> ReservationResponseSchema:
        pass

    @staticmethod
    def update_reservation(
        db: DbSession, reservation_id: uuid.UUID, reservation: ReservationSchema
    ) -> ReservationResponseSchema:
        pass
