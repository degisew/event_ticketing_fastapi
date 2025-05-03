from typing import Any
import uuid

from sqlalchemy import select
from src.core.db import DbSession
from src.core.exceptions import NotFoundException
from src.event.repositories.event import TicketTypeRepository
from src.event.schemas.ticket import TicketTypeSchema, TicketTypeResponseSchema

from src.event.models.event import TicketType


class TicketTypeService:
    @staticmethod
    def create_ticket_types(
        db: DbSession, validated_data: TicketTypeSchema
    ) -> TicketTypeResponseSchema:

        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True)

        remaining_tickets: int | None = serialized_data.get("total_tickets")

        serialized_data["remaining_tickets"] = remaining_tickets

        instance: TicketType = TicketTypeRepository.create(db, serialized_data)

        return TicketTypeResponseSchema.model_validate(instance)

    @staticmethod
    def get_ticket_types(db: DbSession) -> list[TicketTypeResponseSchema]:

        result = TicketTypeRepository.get_ticket_types(db)
        return [
            TicketTypeResponseSchema.model_validate(t_type) for t_type in result
        ]

    @staticmethod
    def get_ticket_type(
        db: DbSession, ticket_type_id: uuid.UUID
    ) -> TicketTypeResponseSchema:
        ticket_type: TicketType | None = TicketTypeRepository.get_ticket_type(
            db,
            ticket_type_id
        )
        if not ticket_type:
            raise NotFoundException("Ticket Type with a given id not found.")

        return TicketTypeResponseSchema.model_validate(ticket_type)

    @staticmethod
    def update_ticket_type(
        db: DbSession, payload: TicketTypeSchema, ticket_type_id: uuid.UUID
    ) -> TicketTypeResponseSchema:
        serialized_data: dict[str, Any] = payload.model_dump(exclude_unset=True)

        ticket_type_obj: TicketType | None = TicketTypeRepository.get_ticket_type(
            db,
            ticket_type_id
        )

        if not ticket_type_obj:
            raise NotFoundException("Ticket Type with a given id not found.")

        result: TicketType = TicketTypeRepository.update_ticket_type(db, serialized_data, ticket_type_obj )

        return TicketTypeResponseSchema.model_validate(result)
