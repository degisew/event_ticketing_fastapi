from typing import Any
import uuid
from src.core.db import DbSession
from src.core.exceptions import NotFoundException
from src.event.repositories.event import EventRepository
from src.event.schemas.event import EventResponseSchema, EventSchema

from src.event.models.event import Event


class EventService:
    @staticmethod
    def create_events(
        db: DbSession, validated_data: EventSchema
    ) -> EventResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True)

        instance = EventRepository.create(db, serialized_data)

        return EventResponseSchema.model_validate(instance)

    @staticmethod
    def get_events(db: DbSession) -> list[EventResponseSchema]:
        result = EventRepository.get_events(db)

        return [
            EventResponseSchema(
                **event.__dict__,
                organizer_email=email
            )
            for event, email in result
        ]

    @staticmethod
    def get_event(db: DbSession, event_id: uuid.UUID) -> EventResponseSchema:
        event: Event | None = EventRepository.get_event(db, event_id)

        if not event:
            raise NotFoundException("Event with a given id not found.")

        return EventResponseSchema.model_validate(event)

    @staticmethod
    def update_event(
        db: DbSession, payload: EventSchema, event_id: uuid.UUID
    ) -> EventResponseSchema:
        serialized_data: dict[str, Any] = payload.model_dump(exclude_unset=True)

        event_obj: Event | None = EventRepository.get_event(db, event_id)

        if not event_obj:
            raise NotFoundException("event with a given id not found.")

        result: Event = EventRepository.update_event(db, serialized_data, event_obj)

        return EventResponseSchema.model_validate(result)
