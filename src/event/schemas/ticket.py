import uuid
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from src.core.schemas import BaseResponseSchema
from src.event.schemas.event import EventSchema


class TicketTypeSchema(BaseModel):
    name: str
    description: str
    price: Decimal
    total_tickets: int

    model_config: ConfigDict = {
        "from_attributes": True
    }


class UpdateTicketTypeSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    total_tickets: int | None = None

    model_config: ConfigDict = {
        "from_attributes": True
    }


class TicketTypeResponseSchema(TicketTypeSchema, BaseResponseSchema):
    remaining_tickets: int
    event_id: uuid.UUID

    model_config: ConfigDict = {
        "from_attributes": True
    }


class TicketSchema(BaseModel):
    price: Decimal
    status: str
    event_id: uuid.UUID
    ticket_type_id: uuid.UUID
    seat_id: uuid.UUID

    model_config: ConfigDict = {
        "from_attributes": True
    }


class TicketResponseSchema(TicketSchema, BaseResponseSchema):
    status: str
    price: Decimal
    ticket: TicketSchema
    event: EventSchema

    model_config: ConfigDict = {
        "from_attributes": True
    }
