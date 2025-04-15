from enum import Enum


class TicketStatuses(Enum):
    TYPE = "ticket_status"

    ACTIVE = "ticket_status_active"

    SOLD = "ticket_status_sold"


class SeatStatuses(Enum):
    TYPE = "seat_status"

    AVAILABLE = "seat_status_available"

    RESERVED = "seat_status_reserved"

    TAKEN = "seat_status_taken"
