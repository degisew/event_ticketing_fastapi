import uuid
from datetime import datetime


class CommonResponseSchema:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
