import uuid
from decimal import Decimal
from pydantic import BaseModel
from src.core.schemas import BaseResponseSchema
from src.event.schemas.event import EventSchema


class TicketTypeSchema(BaseModel):
    name: str
    description: str
    price: Decimal
    total_tickets: int
    event_id: uuid.UUID


class TicketTypeResponseSchema(TicketTypeSchema, BaseResponseSchema):
    remaining_tickets: int

    class Config:
        from_attributes = True


class TicketSchema(BaseModel):
    price: Decimal
    status: str
    event_id: uuid.UUID
    ticket_type_id: uuid.UUID
    seat_id: uuid.UUID


class TicketResponseSchema(TicketSchema, BaseResponseSchema):
    status: str
    price: Decimal
    ticket: TicketSchema
    event: EventSchema

    class Config:
        from_attributes = True
