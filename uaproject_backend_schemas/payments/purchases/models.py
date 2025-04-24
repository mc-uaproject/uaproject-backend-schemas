from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import JSON
from sqlmodel import BigInteger, Column, DateTime, Enum, Field, ForeignKey, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.payments.purchases.schemas import PurchasedItemStatus
from uaproject_backend_schemas.payments.services.models import Service
from uaproject_backend_schemas.payments.transactions.models import Transaction
from uaproject_backend_schemas.webhooks.mixins import (
    WebhookBaseMixin,
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
    WebhookTemporalMixin,
)
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User


__all__ = ["PurchasedItem"]


class PurchasedItem(
    TimestampsMixin,
    IDMixin,
    Base,
    WebhookBaseMixin,
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
    WebhookTemporalMixin,
    table=True,
):
    __tablename__ = "purchased_items"
    __scope_prefix__ = "purchased_item"

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False))
    service_id: int = Field(
        sa_column=Column(BigInteger(), ForeignKey("services.id"), nullable=False)
    )
    transaction_id: int = Field(
        sa_column=Column(BigInteger(), ForeignKey("transactions.id"), nullable=False)
    )
    status: PurchasedItemStatus = Field(
        sa_column=Column(
            Enum(PurchasedItemStatus, native_enum=False),
            default=PurchasedItemStatus.ACTIVE.value,
            server_default=PurchasedItemStatus.ACTIVE.value,
        )
    )
    quantity: int = Field(default=1, ge=1)
    expires_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    purchase_metadata: Optional[Dict[str, Any]] = Field(sa_column=Column(JSON), default=None)

    user: Optional["User"] = Relationship()
    service: Optional["Service"] = Relationship()
    transaction: Optional["Transaction"] = Relationship()

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "full",
            trigger_fields={
                "user_id",
                "service_id",
                "transaction_id",
                "status",
                "quantity",
                "expires_at",
                "purchase_metadata",
            },
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "status",
            trigger_fields={"status"},
            fields={"id", "user_id", "service_id", "status", "expires_at"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "details",
            trigger_fields={"quantity"},
            fields={"id", "user_id", "service_id", "quantity", "status"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "expiration",
            trigger_fields={"expires_at"},
            fields={"id", "user_id", "service_id", "status", "expires_at"},
            stage=WebhookStage.BOTH,
            temporal_fields=[
                {
                    "expires_at_field": "expires_at",
                    "status_field": "status",
                    "status_value": PurchasedItemStatus.EXPIRED.value,
                    "scope_name": "expiration",
                }
            ],
        )

        cls.register_scope(
            "metadata",
            trigger_fields={"purchase_metadata"},
            fields={"id", "user_id", "service_id", "purchase_metadata"},
            stage=WebhookStage.AFTER,
        )
