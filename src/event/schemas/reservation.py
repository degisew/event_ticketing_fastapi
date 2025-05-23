import uuid
from pydantic import BaseModel, ConfigDict
from src.account.schemas import UserResponseSchema
from src.core.schemas import BaseResponseSchema
from src.event.schemas.event import EventSchema
from src.event.schemas.ticket import TicketTypeSchema


class ReservationSchema(BaseModel):
    ticket_quantity: int
    user_id: uuid.UUID
    event_id: uuid.UUID
    ticket_type_id: uuid.UUID

    model_config: ConfigDict = {
        "from_attributes": True
    }


class ReservationResponseSchema(BaseModel, BaseResponseSchema):
    user: UserResponseSchema
    event: EventSchema
    ticket_type: TicketTypeSchema

    model_config: ConfigDict = {
        "from_attributes": True
    }
