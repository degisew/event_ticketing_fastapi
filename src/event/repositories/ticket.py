import uuid
from sqlalchemy import update
from src.core.db import DbSession
from src.event.models.event import Ticket


class TicketRepository:
    @staticmethod
    def create(
        db: DbSession,
        event_id,
        reservation_id,
        ticket_quantity,
        status_id,
        ticket_type_id
    ) -> list[Ticket]:
        tickets: list[Ticket] = [
            Ticket(
                event_id=event_id,
                reservation_id=reservation_id,
                status_id=status_id,
                ticket_type_id=ticket_type_id,
            )
            for _ in range(ticket_quantity)
        ]

        db.add_all(tickets)

        return tickets

    @staticmethod
    def update_ticket_by_reservation_id(
        db: DbSession,
        reservation_id,
        status_id: uuid.UUID
    ) -> None:
        try:
            # Bulk Update ticket status
            db.execute(
                update(Ticket)
                .where(Ticket.reservation_id == reservation_id)
                .values(status_id=status_id)
            )
        except Exception as e:
            print(str(f"DAG Error. {e}"))
            raise e
