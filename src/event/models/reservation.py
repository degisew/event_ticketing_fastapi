import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Uuid, DateTime, String, Integer
from src.account.models import User
from src.core.models import AbstractBaseModel
from src.event.models.event import Event, Seat, TicketType


class Reservation(AbstractBaseModel):
    __tablename__ = "reservations"

    __table_args__ = (
        UniqueConstraint("event_id", "seat_id", name="unq_event_seat_reservation"),
    )

    def default_expiry(self) -> datetime:
        """a helper method for calculating a default
        reservation expiration time.

        Returns:
            datetime
        """
        return datetime.now(timezone.utc) + timedelta(days=1)

    status: Mapped[str] = mapped_column(String(20), nullable=False)

    ticket_quantity: Mapped[int] = mapped_column(Integer(), nullable=False)

    reserved_at: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc)
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False, default=default_expiry
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id"), nullable=False
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("events.id"), nullable=False
    )

    ticket_type_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("ticket_types.id"), nullable=False
    )

    # seat_id: Mapped[uuid.UUID | None] = mapped_column(
    #     Uuid(), ForeignKey("seats.id"), nullable=True
    # )

    # Relationships
    user: Mapped["User"] = relationship()

    event: Mapped["Event"] = relationship()

    ticket_type: Mapped["TicketType"] = relationship()

    # seat: Mapped["Seat"] = relationship()

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def __repr__(self) -> str:
        return f"Reservation({self.id}) - {self.status} - Expires: {self.expires_at.isoformat()}"
