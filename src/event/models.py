import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Uuid,
    DateTime,
    String,
    Integer,
    Text,
    func
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from core.models import AbstractBaseModel
from src.account.models import User


class Event(AbstractBaseModel):
    __tablename__: str = "events"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    organizer_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    organizer: Mapped["User"] = relationship(back_populates="events")

    description: Mapped[str] = mapped_column(Text())

    location: Mapped[str] = mapped_column(String(100))

    venue: Mapped[str] = mapped_column(String(100))

    total_tickets: Mapped[int] = mapped_column(Integer())

    start_time: Mapped[datetime] = mapped_column(DateTime())

    ticket_types: Mapped[list["TicketType"]] = relationship(back_populates="event")

    seats: Mapped[list["Seat"]] = relationship(back_populates="event")

    def __repr__(self) -> str:
        return f"Event {self.name} by {self.organizer.username}"


class TicketType(AbstractBaseModel):
    __tablename__: str = "ticket_types"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str] = mapped_column(Text())

    price: Mapped[int] = mapped_column(Integer())

    total_tickets: Mapped[int] = mapped_column(Integer())

    remaining_tickets: Mapped[int] = mapped_column(Integer())

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("events.id"))

    event: Mapped["Event"] = relationship(back_populates="ticket_types")

    def __repr__(self) -> str:
        return f"{self.name}::{self.total_tickets}"


class Seat(AbstractBaseModel):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint(
            "event_id", "section", "row_number", "seat_number", name="uq_event_seat"
        ),
    )

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("events.id"))

    section: Mapped[str] = mapped_column(String(50), nullable=False)

    row_number: Mapped[int] = mapped_column(Integer(), nullable=True)

    seat_number: Mapped[int] = mapped_column(Integer(), nullable=False)

    is_available: Mapped[bool] = mapped_column(Boolean(), default=True)

    event: Mapped["Event"] = relationship(back_populates="seats")

    def __repr__(self) -> str:
        row = f"Row {self.row_number}" if self.row_number is not None else "No Row"
        return f"Seat {self.section}-{row}-{self.seat_number} ({'Available' if self.is_available else 'Taken'})"


class Ticket(AbstractBaseModel):
    __tablename__: str = "tickets"

    __table_args__ = (UniqueConstraint("seat_id"),)

    event_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("events.id"), nullable=False
    )

    ticket_type_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("ticket_types.id"), nullable=False
    )

    seat_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(), ForeignKey("seats.id"), nullable=False
    )

    price: Mapped[int] = mapped_column(Integer(), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False)

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
        UniqueConstraint("event_id", "seat_id", name="uq_event_seat_reservation"),
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

    status: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    reserved_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now())

    expires_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship()

    event: Mapped["Event"] = relationship()

    ticket_type: Mapped["TicketType"] = relationship()

    seat: Mapped["Seat"] = relationship()

    def __repr__(self) -> str:
        return f"Reservation({self.id}) - {self.status} - Expires: {self.expires_at.isoformat()}"
