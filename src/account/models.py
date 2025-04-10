from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.core.models import AbstractBaseModel


class Role(AbstractBaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"{self.name}"


class User(AbstractBaseModel):
    """
    User model for the application.
    This model represents a user in the system.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True)

    is_superuser: Mapped[bool] = mapped_column(default=False)

    is_profile_complete: Mapped[bool] = mapped_column(default=False)

    profile: Mapped[list["UserProfile"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"{self.username} <{self.email}>"


class UserProfile(AbstractBaseModel):
    """
    User profile model for the application.
    This model represents a user's profile in the system.
    """

    __tablename__ = "user_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="profile")

    first_name: Mapped[str] = mapped_column(nullable=False)

    last_name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
