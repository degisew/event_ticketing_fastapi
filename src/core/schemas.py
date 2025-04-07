import uuid


class CommonResponseSchema:
    id: uuid.UUID
    created_at: str
    updated_at: str
