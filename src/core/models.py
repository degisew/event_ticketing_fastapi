import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func


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

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), default=func.now()
    )
