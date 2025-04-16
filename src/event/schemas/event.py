import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
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

    model_config: ConfigDict = {
        "from_attributes": True
    }


class EventResponseSchema(EventSchema, BaseResponseSchema):
    model_config: ConfigDict = {
        "from_attributes": True
    }
