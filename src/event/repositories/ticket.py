import uuid
from sqlalchemy import select, update
from src.core.db import DbSession
from src.core.logger import logger
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
            logger.exception(str(f"Error: {e}"))
            raise e

    @staticmethod
    def get_tickets_by_reservation(reservation_id: uuid.UUID, db: DbSession):
        return list(db.scalars(
            select(Ticket)
            .where(Ticket.reservation_id == reservation_id)
        ))
