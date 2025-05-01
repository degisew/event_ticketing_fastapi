from enum import Enum


class TransactionPaymentStatuses(Enum):
    COMPLETED = "transaction_payment_status_completed"
    REFUNDED = "transaction_payment_status_refunded"


TRANSACTION_STATUS_TYPE = "transaction_payment_status_type"
