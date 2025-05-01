from sqlalchemy import update
from src.core.db import DbSession
from src.event.models.event import Ticket


class TicketRepository:
    @staticmethod
    def update_ticket_by_reservation_id(
        db: DbSession,
        reservation_id,
        status: str
    ) -> None:
        try:
            # Bulk Update ticket status
            db.execute(
                update(Ticket)
                .where(Ticket.reservation_id == reservation_id)
                .values(status=status)
            )
        except Exception as e:
            print(str(f"Error. {e}"))
            raise e
