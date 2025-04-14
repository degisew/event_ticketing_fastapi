import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    DateTime,
    Numeric,
    Uuid,
    ForeignKey,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.account.models import User
from src.core.models import AbstractBaseModel
from src.event.models import Ticket


class Transaction(AbstractBaseModel):
    __tablename__: str = "transactions"

    __table_args__ = (
        UniqueConstraint("ticket_id", "transaction_date"),)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    payment_status: Mapped[str] = mapped_column(String(20), nullable=False)

    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id"), nullable=False
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("tickets.id"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship()

    ticket: Mapped["Ticket"] = relationship(single_parent=True)

    def __repr__(self) -> str:
        return f"Transaction({self.id}) - {self.payment_status} - ${self.amount}"


class Refund(AbstractBaseModel):
    __tablename__ = "refunds"

    refund_amount: Mapped[int] = mapped_column(Numeric(10, 2), nullable=False)

    refund_status: Mapped[str] = mapped_column(String(20), nullable=False)

    refund_date: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"Refund({self.id}) - ${self.refund_amount} - {self.refund_status}"
