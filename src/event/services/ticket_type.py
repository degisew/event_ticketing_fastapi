from typing import Any
import uuid

from sqlalchemy import select
from src.core.db import DbSession
from src.core.exceptions import NotFoundException
from src.event.schemas.ticket import TicketTypeSchema, TicketTypeResponseSchema

from src.event.models.event import TicketType


class TicketTypeService:
    @staticmethod
    def create_ticket_types(
        db: DbSession, validated_data: TicketTypeSchema
    ) -> TicketTypeResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(exclude_unset=True)

        remaining_tickets = serialized_data.get("total_tickets")

        instance = TicketType(
            **serialized_data,
            remaining_tickets=remaining_tickets
        )

        db.add(instance)
        db.commit()

        db.refresh(instance)

        return TicketTypeResponseSchema.model_validate(instance)

    @staticmethod
    def get_ticket_types(db: DbSession) -> list[TicketTypeResponseSchema]:
        try:
            stmt = select(TicketType)
            result = db.execute(stmt).scalars().all()

            return [
                TicketTypeResponseSchema.model_validate(t_type) for t_type in result
            ]
        except Exception as e:
            raise e

    @staticmethod
    def get_ticket_type(
        db: DbSession, ticket_type_id: uuid.UUID
    ) -> TicketTypeResponseSchema:
        ticket_type: TicketType | None = db.get(TicketType, ticket_type_id)

        if not ticket_type:
            raise NotFoundException("Ticket Type with a given id not found.")

        return TicketTypeResponseSchema.model_validate(ticket_type)

    @staticmethod
    def update_ticket_type(
        db: DbSession, ticket_type: TicketTypeSchema, ticket_type_id: uuid.UUID
    ) -> TicketTypeResponseSchema:
        serialized_data = ticket_type.model_dump(exclude_unset=True)

        ticket_type_obj: TicketType | None = db.get(TicketType, ticket_type_id)

        if not ticket_type:
            raise NotFoundException("Ticket Type with a given id not found.")

        for key, val in serialized_data.items():
            if getattr(ticket_type_obj, key) != val:
                setattr(ticket_type_obj, key, val)

        db.commit()
        db.refresh(ticket_type_obj)

        return TicketTypeResponseSchema.model_validate(ticket_type_obj)
