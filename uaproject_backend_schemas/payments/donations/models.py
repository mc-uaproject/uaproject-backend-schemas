from typing import Optional

from sqlmodel import DECIMAL, BigInteger, Column, Field

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.schemas import SerializableDecimal
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["Donation"]


class Donation(TimestampsMixin, IDMixin, Base, WebhookPayloadMixin, table=True):
    __tablename__ = "donations"
    __scope_prefix__ = "donation"

    user_id: int = Field(foreign_key="users.id", sa_column=Column(BigInteger(), nullable=False))
    balance_id: int = Field(foreign_key="balances.id", sa_column=Column(BigInteger(), nullable=False))
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
