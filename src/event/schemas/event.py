import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.core.schemas import BaseResponseSchema


class EventSchema(BaseModel):
    name: str
    description: str
    location: str
    venue: str
    total_tickets: int
    start_time: datetime
    end_time: datetime

    model_config: ConfigDict = {
        "from_attributes": True
    }


class UpdateEventSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    venue: str | None = None
    total_tickets: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class EventResponseSchema(EventSchema, BaseResponseSchema):
    organizer_email: str

    model_config: ConfigDict = {
        "from_attributes": True
    }
