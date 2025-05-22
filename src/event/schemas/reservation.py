import uuid
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.account.schemas import UserResponseSchema
from src.core.schemas import BaseResponseSchema, DataLookupResponseSchema
from src.event.schemas.ticket import TicketTypeSchema


class ReservationSchema(BaseModel):
    ticket_quantity: int
    ticket_type_id: uuid.UUID

    model_config: ConfigDict = {
        "from_attributes": True
    }


class ReservationResponseSchema(BaseModel, BaseResponseSchema):
    user: UserResponseSchema
    ticket_type: TicketTypeSchema
    ticket_quantity: int
    model_config: ConfigDict = {
        "from_attributes": True
    }


class CheckoutSummaryResponseSchema(BaseModel):
    reservation_id: uuid.UUID
    ticket_type: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class PurchaseRequestSchema(BaseModel):
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
