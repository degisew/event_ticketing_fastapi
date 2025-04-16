from fastapi.routing import APIRouter
from sqlalchemy import select

from src.core.db import DbSession
from src.core.models import DataLookup
from src.core.schemas import DataLookupResponseSchema, DataLookupSchema


router = APIRouter()


@router.post("/data_lookups")
async def create_data_lookups(
    db: DbSession, payload: DataLookupSchema
) -> DataLookupResponseSchema:
    serialized_data = payload.model_dump(exclude_unset=True)

    instance = DataLookup(**serialized_data)

    db.add(instance)

    db.commit()

    db.refresh(instance)

    return DataLookupResponseSchema.model_validate(instance)


@router.get("/data_lookups")
async def get_data_lookups(db: DbSession) -> list[DataLookupResponseSchema]:
    result = db.scalars(
        select(DataLookup)
    ).all()

    return [DataLookupResponseSchema.model_validate(res) for res in result]
