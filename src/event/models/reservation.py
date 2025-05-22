from decimal import Decimal
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    Uuid,
    DateTime,
    Integer
)
from src.account.models import User
from src.core.models import AbstractBaseModel, DataLookup
from src.event.models.event import Event, Ticket, TicketType


class Reservation(AbstractBaseModel):
    __tablename__ = "reservations"

    def default_expiry(self) -> datetime:
        """a helper method for calculating a default
        reservation expiration time.

        Returns:
            datetime
        """
        return datetime.now(timezone.utc) + timedelta(minutes=15)

    status_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(), ForeignKey("data_lookups.id")
    )

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

    # Relationships
    user: Mapped["User"] = relationship()

    event: Mapped["Event"] = relationship()

    ticket_type: Mapped["TicketType"] = relationship()

    tickets: Mapped["Ticket"] = relationship()

    status: Mapped["DataLookup"] = relationship()

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def mark_as_completed(self, reservation_status) -> None:
        self.status = reservation_status

    def __repr__(self) -> str:
        return f"Reservation({self.id}) - {self.status} - Expires: {self.expires_at.isoformat()}"


class Transaction(AbstractBaseModel):
    __tablename__: str = "transactions"

    __table_args__ = (
        UniqueConstraint("transaction_date"),)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    payment_status_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(), ForeignKey("data_lookups.id")
    )

    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id"), nullable=False
    )

    reservation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("reservations.id"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship()

    payment_status: Mapped["DataLookup"] = relationship()

    reservation: Mapped["Reservation"] = relationship(single_parent=True)

    def __repr__(self) -> str:
        return f"Transaction({self.id}) - {self.payment_status} - ${self.amount}"
