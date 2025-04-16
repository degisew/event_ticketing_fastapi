import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseResponseSchema:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DataLookupSchema(BaseModel):
    type: str
    name: str
    value: str
    description: str
    remark: str


class DataLookupResponseSchema(DataLookupSchema, BaseResponseSchema):
    model_config: ConfigDict = {
        "from_attributes": True
    }
