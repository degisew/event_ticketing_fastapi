import uuid
from datetime import datetime


class BaseResponseSchema:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
