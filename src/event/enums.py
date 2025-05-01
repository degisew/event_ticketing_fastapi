from enum import Enum


class SeatStatuses(Enum):
    AVAILABLE = "seat_status_available"
    RESERVED = "seat_status_reserved"
    TAKEN = "seat_status_taken"


class ReservationPaymentStatuses(Enum):
    PENDING = "reservation_payment_status_pending"
    PAID = "reservation_payment_status_paid"
    CANCELED = "reservation_payment_status_canceled"
    REFUNDED = "reservation_payment_status_refunded"


class ReservationStatuses(Enum):
    CONFIRMED = "reservation_status_confirmed"
    CANCELED = "reservation_status_canceled"
    COMPLETED = "reservation_status_completed"
    REFUNDED = "reservation_status_refunded"


class TicketStatuses(Enum):
    ACTIVE = "ticket_status_active"
    SOLD = "ticket_status_sold"


class TicketTypes(Enum):
    NORMAL = "ticket_type_normal"
    VIP = "ticket_type_vip"


# * I do this instead of storing TYPE inside the enums is b/c
# * semantically, TYPE is not an enum——it’s metadata about the enum group.
RESERVATION_STATUS_TYPE = "reservation_status"
TICKET_STATUS_TYPE = "ticket_status"
TICKET_TYPES_TYPE = "ticket_type_type"
RESERVATION_PAYMENT_STATUS_TYPE = "reservation_payment_status"
SEAT_STATUS_TYPE = "seat_status"
