import uuid
from pydantic import BaseModel
from src.account.schemas import UserSchema
from src.core.schemas import BaseResponseSchema
from src.event.schemas.event import EventSchema
from src.event.schemas.ticket import TicketTypeSchema


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
