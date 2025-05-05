from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlmodel import DECIMAL, JSON, BigInteger, Column, Enum, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.transaction import TransactionType

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.service import Service
    from uaproject_backend_schemas.models.user import User


class Transaction(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "transactions"
    __scope_prefix__ = "transaction"

    user_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )
    amount: Decimal = AwesomeField(sa_column=Column(DECIMAL(10, 2), nullable=False))
    type: TransactionType = AwesomeField(sa_column=Column(Enum(TransactionType, native_enum=False)))
    description: Optional[str] = AwesomeField(max_length=255, nullable=True)
    recipient_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )
    service_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("services.id"), nullable=True)
    )
    transaction_metadata: Optional[Dict[str, Any]] = AwesomeField(
        sa_column=Column(JSON, nullable=True)
    )

    service: Optional["Service"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Transaction.service_id]"}
    )
    user: Optional["User"] = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.user_id]"},
    )
    recipient: Optional["User"] = Relationship(
        back_populates="received_transactions",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.recipient_id]"},
    )
