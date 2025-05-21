from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict
from src.account.schemas import UserResponseSchema
from src.core.schemas import BaseResponseSchema, DataLookupResponseSchema
from src.event.schemas.event import EventSchema
from src.event.schemas.ticket import TicketTypeSchema


class ReservationSchema(BaseModel):
    ticket_quantity: int
    # user_id: uuid.UUID
    # event_id: uuid.UUID
    ticket_type_id: uuid.UUID

    model_config: ConfigDict = {
        "from_attributes": True
    }


class ReservationResponseSchema(BaseModel, BaseResponseSchema):
    user: UserResponseSchema
    # event: EventSchema
    ticket_type: TicketTypeSchema

    model_config: ConfigDict = {
        "from_attributes": True
    }


class PurchaseRequestSchema(BaseModel):
    # user_id: UUID
    payment_method: str
    amount: Decimal


class PurchaseResponseSchema(BaseResponseSchema, PurchaseRequestSchema):
    reservation_id: uuid.UUID
    user_id: uuid.UUID
    model_config: ConfigDict = {
        "from_attributes": True
    }


class TransactionResponseSchema(BaseModel, BaseResponseSchema):
    transaction_date: datetime
    # TODO: consider doing this amount calculation in the backend
    amount: Decimal
    reservation: ReservationSchema
    payment_method: str
    payment_status: DataLookupResponseSchema

    model_config: ConfigDict = {
        "from_attributes": True
    }
