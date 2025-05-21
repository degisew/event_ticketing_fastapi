# from datetime import datetime
# from uuid import UUID
# from decimal import Decimal
# from pydantic import BaseModel, ConfigDict

# from src.core.schemas import BaseResponseSchema, DataLookupResponseSchema
# from src.event.schemas.reservation import ReservationSchema


# class PurchaseRequestSchema(BaseModel):
#     # user_id: UUID
#     payment_method: str
#     amount: Decimal


# class PurchaseResponseSchema(BaseResponseSchema, PurchaseRequestSchema):
#     reservation_id: UUID
#     user_id: UUID
#     model_config: ConfigDict = {
#         "from_attributes": True
#     }


# class TransactionResponseSchema(BaseModel, BaseResponseSchema):
#     transaction_date: datetime
#     # TODO: consider doing this amount calculation in the backend
#     amount: Decimal
#     reservation: ReservationSchema
#     payment_method: str
#     payment_status: DataLookupResponseSchema

#     model_config: ConfigDict = {
#         "from_attributes": True
#     }
