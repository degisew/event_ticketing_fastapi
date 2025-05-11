import uuid
from sqlalchemy import (
    Uuid,
    ForeignKey,
    String,
    Boolean,
    UniqueConstraint
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.models import AbstractBaseModel


class Role(AbstractBaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name}"


class User(AbstractBaseModel):
    """
    User model for the application.
    This model represents a user in the system.
    """

    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("role_id", "id"),
    )
    # TODO: Remove username
    username: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    role_id: Mapped[uuid.UUID] = mapped_column(Uuid(),  ForeignKey("roles.id"))

    password: Mapped[str] = mapped_column(String(100), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)

    is_profile_complete: Mapped[bool] = mapped_column(Boolean(), default=False)

    # Relationships
    role: Mapped["Role"] = relationship(single_parent=True)

    profile: Mapped["UserProfile"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"{self.username} <{self.email}>"


class UserProfile(AbstractBaseModel):
    """
    User profile model for the application.
    This model represents a user's profile in the system.
    """

    __tablename__ = "user_profiles"

    # Forcing one-to-one in db level
    __table_args__ = (UniqueConstraint("user_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="profile", single_parent=True)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
