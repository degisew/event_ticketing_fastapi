from typing import Any
import uuid

from sqlalchemy import select
from src.core.db import DbSession
from src.core.exceptions import NotFoundException
from src.event.schemas.event import EventResponseSchema, EventSchema

from src.event.models.event import Event


class EventService:
    @staticmethod
    def create_events(
        db: DbSession, validated_data: EventSchema
    ) -> EventResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(exclude_unset=True)
        instance = Event(**serialized_data)

        db.add(instance)
        db.commit()

        db.refresh(instance)

        return EventResponseSchema.model_validate(instance)

    @staticmethod
    def get_events(db: DbSession) -> list[EventResponseSchema]:
        try:
            stmt = select(Event)
            result = db.execute(stmt).scalars().all()

            return [EventResponseSchema.model_validate(user) for user in result]
        except Exception as e:
            raise e

    @staticmethod
    def get_event(db: DbSession, event_id: uuid.UUID) -> EventResponseSchema:
        event: Event | None = db.get(Event, event_id)

        if not event:
            raise NotFoundException("Event with a given id not found.")

        return EventResponseSchema.model_validate(event)

    @staticmethod
    def update_event(
        db: DbSession, event: EventSchema, event_id: uuid.UUID
    ) -> EventResponseSchema:
        serialized_data = event.model_dump(exclude_unset=True)

        event_obj: Event | None = db.get(Event, event_id)

        if not event:
            raise NotFoundException("event with a given id not found.")

        for key, val in serialized_data.items():
            if getattr(event_obj, key) != val:
                setattr(event_obj, key, val)

        db.commit()
        db.refresh(event_obj)

        return EventResponseSchema.model_validate(event_obj)
