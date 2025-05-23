from typing import TYPE_CHECKING, Optional

from sqlmodel import DECIMAL, BigInteger, Column, Field, ForeignKey

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.schemas import SerializableDecimal
from uaproject_backend_schemas.webhooks.mixins import WebhookChangesMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    pass

__all__ = ["Donation"]


class Donation(
    TimestampsMixin,
    IDMixin,
    Base,
    WebhookChangesMixin,
    table=True,
):
    __tablename__ = "donations"
    __scope_prefix__ = "donation"

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False))
    balance_id: int = Field(
        sa_column=Column(BigInteger(), ForeignKey("balances.id"), nullable=False)
    )
    amount: SerializableDecimal = Field(sa_column=Column(DECIMAL(10, 2), nullable=False))
    currency: str = Field(max_length=3)
    donor_name: str = Field(max_length=255)
    donor_email: Optional[str] = Field(max_length=255, nullable=True)
    message: str = Field(max_length=1000)
    source: str = Field(max_length=50)
    donatello_transaction_id: str = Field(unique=True)

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "created",
            trigger_fields={
                "user_id",
                "amount",
                "currency",
                "donor_name",
                "donor_email",
                "message",
                "source",
                "donatello_transaction_id",
            },
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "updated",
            trigger_fields={"amount", "currency", "donor_name", "donor_email", "message"},
            fields={
                "id",
                "user_id",
                "amount",
                "currency",
                "donor_name",
                "donor_email",
                "message",
                "source",
                "donatello_transaction_id",
            },
            stage=WebhookStage.BOTH,
        )
