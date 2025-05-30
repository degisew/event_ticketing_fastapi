from typing import Any
from uuid import UUID
from sqlalchemy import ScalarResult, select
from src.account.models import User
from src.core.db import DbSession
from src.core.logger import logger
from src.event.models.event import Event, TicketType


class EventRepository:
    @staticmethod
    def create(db: DbSession, serialized_data) -> Event:
        instance = Event(**serialized_data)

        db.add(instance)
        db.commit()

        db.refresh(instance)

        return instance

    @staticmethod
    def get_events(db: DbSession):
        try:
            events = (
                db.query(
                    Event,
                    User.email.label("organizer_email")
                )
                .join(User, Event.organizer_id == User.id)
                .all()
            )
            return events
        except Exception as e:
            logger.exception(f"Error: {str(e)}")
            raise e

    @staticmethod
    def get_event(db: DbSession, event_id: UUID) -> Event | None:
        event: Event | None = db.get(Event, event_id)
        return event

    @staticmethod
    def update_event(
        db: DbSession,
        serialized_data: dict[str, Any],
        event_obj
    ) -> Event:
        for key, val in serialized_data.items():
            if getattr(event_obj, key) != val:
                setattr(event_obj, key, val)

        db.commit()
        db.refresh(event_obj)

        return event_obj


class TicketTypeRepository:
    @staticmethod
    def create(db: DbSession, serialized_data: dict[str, Any]) -> TicketType:
        instance = TicketType(**serialized_data)

        db.add(instance)
        db.commit()

        db.refresh(instance)

        return instance

    @staticmethod
    def get_ticket_types(db: DbSession, event_id: UUID):
        try:
            result = db.scalars(
                select(TicketType)
                .where(TicketType.event_id == event_id)
            )

            return result
        except Exception as e:
            logger.exception(f"Error: {str(e)}")
            raise e

    @staticmethod
    def get_ticket_type(
        db: DbSession,
        event_id: UUID,
        ticket_type_id: UUID,
        locking_needed: bool = False
    ) -> TicketType | None:
        # Avoiding unncessesary locking
        if locking_needed:
            # * trigger db row-locking using sqlalchemy with_for_update()
            # * to prevent race codition that leads to overbooking
            t_type: TicketType | None = db.scalar(
                select(TicketType)
                .where(
                    TicketType.id == ticket_type_id,
                    TicketType.event_id == event_id
                )
                .with_for_update()  # row-locking happens here
            )
        else:
            t_type: TicketType | None = db.scalar(
                select(TicketType)
                .where(
                    TicketType.id == ticket_type_id,
                    TicketType.event_id == event_id
                )
            )

        return t_type

    @staticmethod
    def update_ticket_type(
            db: DbSession,
            serialized_data: dict[str, Any],
            ticket_type_obj: TicketType
    ) -> TicketType:
        try:
            for key, val in serialized_data.items():
                if getattr(ticket_type_obj, key) != val:
                    setattr(ticket_type_obj, key, val)
            db.commit()
            db.refresh(ticket_type_obj)

            return ticket_type_obj
        except Exception as e:
            logger.exception(f"Error {str(e)}")
            raise e
