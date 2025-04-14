import uuid
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Uuid,
    DateTime,
    String,
    Integer,
    Numeric,
    Text
)
from src.account.models import User
from src.core.models import AbstractBaseModel


class Event(AbstractBaseModel):
    __tablename__: str = "events"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    organizer_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    organizer: Mapped["User"] = relationship(back_populates="events")

    description: Mapped[str] = mapped_column(Text())

    location: Mapped[str] = mapped_column(String(100), nullable=False)

    venue: Mapped[str] = mapped_column(String(100), nullable=False)

    total_tickets: Mapped[int] = mapped_column(Integer(), nullable=False)

    start_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    end_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # Relationships
    ticket_types: Mapped[list["TicketType"]] = relationship(back_populates="event")

    seats: Mapped[list["Seat"]] = relationship(back_populates="event")

    def __repr__(self) -> str:
        return f"Event {self.name} by {self.organizer.username}"


class TicketType(AbstractBaseModel):
    __tablename__: str = "ticket_types"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str] = mapped_column(Text(), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    total_tickets: Mapped[int] = mapped_column(Integer(), nullable=False)

    remaining_tickets: Mapped[int] = mapped_column(Integer())

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("events.id"))

    # Relationships
    event: Mapped["Event"] = relationship(back_populates="ticket_types")

    def __repr__(self) -> str:
        return f"{self.name}::{self.total_tickets}"


class Seat(AbstractBaseModel):
    __tablename__ = "seats"

    __table_args__ = (
        UniqueConstraint(
            "event_id", "section", "seat_number", name="unq_event_seat"
        ),
    )

    section: Mapped[str] = mapped_column(String(50), nullable=False)

    row_number: Mapped[int] = mapped_column(Integer(), nullable=True)

    seat_number: Mapped[int] = mapped_column(Integer(), nullable=False)

    is_available: Mapped[bool] = mapped_column(Boolean(), default=True)

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("events.id"))

    # Relationships
    event: Mapped["Event"] = relationship(back_populates="seats")

    def __repr__(self) -> str:
        row = f"Row {self.row_number}" if self.row_number is not None else "No Row"
        return f"Seat {self.section}-{row}-{self.seat_number} ({'Available' if self.is_available else 'Taken'})"


class Ticket(AbstractBaseModel):
    __tablename__: str = "tickets"

    __table_args__ = (UniqueConstraint("seat_id"),)

    price: Mapped[int] = mapped_column(Integer(), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False)

    event_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("events.id"), nullable=False
    )

    ticket_type_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("ticket_types.id"), nullable=False
    )

    seat_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("seats.id"), nullable=False
    )

    # Relationships
    event: Mapped["Event"] = relationship(back_populates="tickets")

    ticket_type: Mapped["TicketType"] = relationship(back_populates="tickets")

    seat: Mapped["Seat"] = relationship(
        back_populates="ticket", single_parent=True
    )

    def __repr__(self) -> str:
        return f"Ticket {self.status} - ${self.price}"


class Reservation(AbstractBaseModel):
    __tablename__ = "reservations"

    __table_args__ = (
        UniqueConstraint(
            "event_id", "seat_id", name="unq_event_seat_reservation"
        ),
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

    seat_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(), ForeignKey("seats.id"), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship()

    event: Mapped["Event"] = relationship()

    ticket_type: Mapped["TicketType"] = relationship()

    seat: Mapped["Seat"] = relationship()

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def __repr__(self) -> str:
        return f"Reservation({self.id}) - {self.status} - Expires: {self.expires_at.isoformat()}"
