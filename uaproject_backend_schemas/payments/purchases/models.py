from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum
from sqlmodel import BigInteger, Column, Field, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.payments.purchases.schemas import PurchasedItemStatus
from uaproject_backend_schemas.payments.services.models import Service
from uaproject_backend_schemas.payments.transactions.models import Transaction
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User


__all__ = ["PurchasedItem"]

class PurchasedItem(TimestampsMixin, IDMixin, Base, WebhookPayloadMixin, table=True):
    __tablename__ = "purchased_items"
    __scope_prefix__ = "purchased_item"

    user_id: int = Field(foreign_key="users.id", sa_column=Column(BigInteger(), nullable=False))
    service_id: int = Field(foreign_key="services.id", sa_column=Column(BigInteger(), nullable=False))
    transaction_id: int = Field(foreign_key="transactions.id", nullable=False)
    status: PurchasedItemStatus = Field(
        sa_column=Column(
            Enum(PurchasedItemStatus, native_enum=False),
            default=PurchasedItemStatus.ACTIVE.value,
            server_default=PurchasedItemStatus.ACTIVE.value,
        )
    )
    quantity: int = Field(default=1, ge=1)
    time_spent: int = Field(default=0, ge=0)

    user: Optional["User"] = Relationship()
    service: Optional["Service"] = Relationship()
    transaction: Optional["Transaction"] = Relationship()

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "full",
            trigger_fields={"user_id", "service_id", "transaction_id", "status", "quantity"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "status",
            trigger_fields={"status"},
            fields={"id", "user_id", "service_id", "status"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "details",
            trigger_fields={"quantity"},
            fields={"id", "user_id", "service_id", "quantity", "status", "time_spent"},
            stage=WebhookStage.BOTH,
        )
