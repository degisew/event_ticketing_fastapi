from enum import Enum


class SeatStatuses(Enum):
    TYPE = "seat_status"
    AVAILABLE = "seat_status_available"
    RESERVED = "seat_status_reserved"
    TAKEN = "seat_status_taken"


class ReservationPaymentStatuses(Enum):
    TYPE = "reservation_payment_status"
    PENDING = "reservation_payment_status_pending"
    PAID = "reservation_payment_status_paid"
    CANCELED = "reservation_payment_status_canceled"
    REFUNDED = "reservation_payment_status_refunded"


class ReservationStatuses(Enum):
    TYPE = "reservation_status"
    CONFIRMED = "reservation_status_confirmed"
    CANCELED = "reservation_status_canceled"
    COMPLETED = "reservation_status_completed"
    REFUNDED = "reservation_status_refunded"


class TicketStatuses(Enum):
    TYPE = "ticket_status"
    ACTIVE = "ticket_status_active"
    SOLD = "ticket_status_sold"


class TicketTypes(Enum):
    TYPE = "ticket_type_type"
    NORMAL = "ticket_type_normal"
    VIP = "ticket_type_vip"
