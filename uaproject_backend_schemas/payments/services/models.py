from typing import List, Optional

from sqlmodel import DECIMAL, JSON, Column, Enum, Field

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.payments.services.schemas import (
    ServiceDiscount,
    ServiceMetadata,
    ServicePoints,
    ServiceType,
)
from uaproject_backend_schemas.schemas import SerializableDecimal
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["Service"]


class Service(TimestampsMixin, IDMixin, Base, WebhookPayloadMixin, table=True):
    __tablename__ = "services"
    __scope_prefix__ = "service"

    name: str = Field(max_length=255, unique=True, nullable=False)
    display_name: Optional[str] = Field(max_length=255, nullable=True)
    description: Optional[str] = Field(max_length=1000, nullable=True)
    points: Optional[List[ServicePoints]] = Field(sa_column=Column(JSON), default=None)
    image: Optional[str] = Field(max_length=500, nullable=True)
    price: SerializableDecimal = Field(sa_column=Column(DECIMAL(10, 2), nullable=False))
    currency: str = Field(max_length=3, default="UAH")
    is_active: bool = Field(default=True)
    category: Optional[str] = Field(max_length=100, nullable=True)
    type: ServiceType = Field(sa_column=Column(Enum(ServiceType, native_enum=False)))
    duration_months: Optional[int] = Field(nullable=True)
    is_upgradable: bool = Field(default=False)
    upgrade_from: Optional[str] = Field(max_length=100, nullable=True)
    upgrade_to: Optional[str] = Field(max_length=100, nullable=True)
    service_metadata: Optional[ServiceMetadata] = Field(sa_column=Column(JSON), default=None)
    discounts: Optional[List[ServiceDiscount]] = Field(sa_column=Column(JSON), default=None)

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "full",
            trigger_fields={
                "name", "display_name", "description", "points", "image",
                "price", "currency", "is_active", "category", "type",
                "duration_months", "is_upgradable", "upgrade_from", "upgrade_to",
                "service_metadata", "discounts"
            },
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "status",
            trigger_fields={"is_active"},
            fields={"id", "name", "display_name", "is_active"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "price",
            trigger_fields={"price"},
            fields={"id", "name", "display_name", "price", "currency"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "content",
            trigger_fields={"description", "points", "image"},
            fields={"id", "name", "display_name", "description", "points", "image"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "discounts",
            trigger_fields={"discounts"},
            fields={"id", "name", "display_name", "discounts"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "upgrade",
            trigger_fields={"is_upgradable", "upgrade_from", "upgrade_to"},
            fields={"id", "name", "display_name", "is_upgradable", "upgrade_from", "upgrade_to"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "metadata",
            trigger_fields={"service_metadata"},
            fields={"id", "name", "display_name", "service_metadata"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "subscription",
            trigger_fields={"type", "duration_months"},
            fields={"id", "name", "display_name", "type", "duration_months"},
            stage=WebhookStage.AFTER,
        )
