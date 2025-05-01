from datetime import datetime
from decimal import Decimal
import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    Uuid,
    String,
    Integer,
    Text,
)

from src.account.models import User
from src.core.models import AbstractBaseModel, DataLookup


class Event(AbstractBaseModel):
    __tablename__: str = "events"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    organizer_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    description: Mapped[str] = mapped_column(Text())

    location: Mapped[str] = mapped_column(String(100), nullable=False)

    venue: Mapped[str] = mapped_column(String(100), nullable=False)

    total_tickets: Mapped[int] = mapped_column(Integer(), nullable=False)

    start_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    end_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # Relationships
    organizer: Mapped["User"] = relationship()

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

    def set_remaining_ticketon_first_creation(self) -> None:
        self.remaining_tickets = self.total_tickets

    def update_remaining_tickets(self, quantity: int) -> None:
        self.remaining_tickets -= quantity

    def __repr__(self) -> str:
        return f"{self.name}::{self.total_tickets}"


class Seat(AbstractBaseModel):
    __tablename__ = "seats"

    __table_args__ = (
        UniqueConstraint("event_id", "section", "seat_number", name="unq_event_seat"),
    )

    section: Mapped[str] = mapped_column(String(50), nullable=False)

    row_number: Mapped[int] = mapped_column(Integer(), nullable=True)

    seat_number: Mapped[int] = mapped_column(Integer(), nullable=False)

    status_id: Mapped[str] = mapped_column(Uuid(), ForeignKey("data_lookups.id"))

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("events.id"))

    # Relationships
    status: Mapped["DataLookup"] = relationship()

    event: Mapped["Event"] = relationship(back_populates="seats")

    ticket: Mapped["Ticket"] = relationship(back_populates="seat")

    def __repr__(self) -> str:
        row = f"Row {self.row_number}" if self.row_number is not None else "No Row"
        return f"Seat {self.section}-{row}-{self.seat_number} ({'Available' if self.is_available else 'Taken'})"


class Ticket(AbstractBaseModel):
    __tablename__: str = "tickets"

    __table_args__ = (UniqueConstraint("seat_id"),)

    # TODO: May be it's better to remove this price attr since
    # TODO: it's in the ticket type
    # price: Mapped[int] = mapped_column(Integer(), nullable=False)
    status_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("data_lookups.id"), nullable=False
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("events.id"), nullable=False
    )

    ticket_type_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("ticket_types.id"), nullable=False
    )

    seat_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("seats.id"), nullable=True
    )

    reservation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("reservations.id"), nullable=False
    )
    # Relationships
    status: Mapped["DataLookup"] = relationship()

    event: Mapped["Event"] = relationship()

    ticket_type: Mapped["TicketType"] = relationship()

    seat: Mapped["Seat"] = relationship(back_populates="ticket", single_parent=True)

    def __repr__(self) -> str:
        return f"Ticket {self.status} - ${self.ticket_type}"
