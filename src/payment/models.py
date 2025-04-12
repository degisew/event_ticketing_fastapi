from datetime import datetime
import uuid
from sqlalchemy import (
    DateTime,
    Integer,
    Uuid,
    ForeignKey,
    String,
    func,
    UniqueConstraint
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.account.models import User
from src.core.models import AbstractBaseModel
from src.event.models import Ticket


class Transaction(AbstractBaseModel):
    __tablename__: str = "transactions"

    __table_args__ = (
        UniqueConstraint("refund"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id"), nullable=False
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("tickets.id"), nullable=False
    )

    amount: Mapped[int] = mapped_column(Integer(), nullable=False)

    payment_status: Mapped[str] = mapped_column(String(20), nullable=False)

    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )

    refund_status: Mapped[str] = mapped_column(String(20), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship()

    refund: Mapped["Refund"] = relationship(
        back_populates="transaction", single_parent=True
    )

    ticket: Mapped["Ticket"] = relationship()

    def __repr__(self) -> str:
        return f"Transaction({self.id}) - {self.payment_status} - ${self.amount}"


class Refund(AbstractBaseModel):
    __tablename__ = "refunds"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("transactions.id"), nullable=False
    )

    refund_amount: Mapped[int] = mapped_column(Integer(), nullable=False)

    refund_status: Mapped[str] = mapped_column(String(20), nullable=False)

    refund_date: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    # Relationships
    transaction: Mapped["Transaction"] = relationship(back_populates="refund")

    def __repr__(self) -> str:
        return f"Refund({self.id}) - ${self.refund_amount} - {self.refund_status}"
