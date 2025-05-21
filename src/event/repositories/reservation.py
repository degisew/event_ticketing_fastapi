from typing import Any
from uuid import UUID
from sqlalchemy import select
from src.core.db import DbSession
from src.event.models.reservation import Reservation


class ReservationRepository:
    @staticmethod
    def create(
        db: DbSession,
        serialized_data: dict[str, Any]
    ) -> Reservation:
        reservation = Reservation(**serialized_data)

        db.add(reservation)
        # * flushing reservation to get the id
        # * but it can be rolled back if smtg happens.
        db.flush()

        return reservation

    @staticmethod
    def get_reservations(
        db: DbSession,
        event_id: UUID,
    ):
        result = db.scalars(
            select(Reservation)
            .where(Reservation.event_id == event_id)
        )

        return result

    @staticmethod
    def get_reservations_by_user(db: DbSession, user_id: UUID):
        result = db.scalars(
            select(Reservation)
            .where(Reservation.user_id == user_id)
        )

        return result
