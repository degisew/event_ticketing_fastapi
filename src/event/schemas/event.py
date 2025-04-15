import uuid
from datetime import datetime
from pydantic import BaseModel
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
