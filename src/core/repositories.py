from sqlalchemy import select, update
from src.core.db import DbSession
from src.core.models import DataLookup
from src.event.enums import ReservationStatuses, TicketStatuses


# TODO: CAche them in memory since this are static.
# TODO: load to dict on startup or use tools like redis


class DataLookupRepository:
    """A Repository class for handling Data access and Manipulation logic.
    It helps to separate Data related logic from the service
    and also avoids direct interaction to data store.
    """

    @staticmethod
    def get_status_by_type(db: DbSession, type_: str, value: str) -> DataLookup | None:
        """A method that fetches a specific DataLookup instance by a given type.

        Args:
            db (DbSession): Database session dependancy.
            type_ (str): a datalookup type.
            value (str): a datalookup value for a given type.

        Returns:
            DataLookup | None: If the query matches, It returns a DataLookup or None.
        """
        return db.scalar(
            select(DataLookup).where(
                DataLookup.type == type_,
                DataLookup.value == value,
            )
        )
