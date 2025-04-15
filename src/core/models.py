import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, Text, func, DateTime, Uuid, UniqueConstraint


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models.
    This class is used to create the declarative base for the ORM.
    """

    pass


class AbstractBaseModel(Base):
    """
    Abstract base model for all database models.
    This class provides common fields and methods for all models.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), onupdate=func.now(), default=func.now()
    )


class DataLookup(AbstractBaseModel):
    """A sqlalchemy model for storing global lookup data
    that will be used as enums across the project.

    Args:
        AbstractBaseModel (Base): A Parent class for all sqlalchemy models
    """

    __tablename__: str = "data_lookups"

    __table_args__ = (UniqueConstraint("type", "value"),)

    type: Mapped[str] = mapped_column(String(100), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    value: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(Text())

    remark: Mapped[str] = mapped_column(String(100))
