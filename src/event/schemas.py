import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from src.account.schemas import UserSchema
from src.core.schemas import BaseResponseSchema


class EventSchema(BaseModel):
    name: str
    description: str
    organizer_id: uuid.UUID
    location: str
    venue: str
    total_tickets: int
    start_time: datetime
    end_time: datetime


class EventResponseSchema(EventSchema, BaseResponseSchema):
    class Config:
        from_attributes = True


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


class ReservationSchema(BaseModel):
    status: str
    ticket_quantity: int
    user_id: uuid.UUID
    event_id: uuid.UUID
    ticket_type_id: uuid.UUID


class ReservationResponseSchema(BaseResponseSchema):
    status: str
    user: UserSchema
    event: EventSchema
    tickt_type: TicketTypeSchema

    class Config:
        from_attributes = True
