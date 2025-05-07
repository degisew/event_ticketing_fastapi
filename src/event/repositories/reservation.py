from typing import Any
from sqlalchemy import select
from src.core.db import DbSession
from src.event.models.reservation import Reservation


class ReservationRepository:
    @staticmethod
    def create(db: DbSession, serialized_data: dict[str, Any]) -> Reservation:
        reservation = Reservation(**serialized_data)

        db.add(reservation)
        # * flushing reservation to get the id
        # * but it can be rolled back if smtg happens.
        db.flush()

        return reservation

    @staticmethod
    def get_reservations(db: DbSession):
        result = db.scalars(
            select(Reservation)
        )

        return result
