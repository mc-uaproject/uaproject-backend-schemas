from typing import Optional

from sqlmodel import DECIMAL, Column, Field

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.schemas import SerializableDecimal
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["Service"]


class Service(TimestampsMixin, IDMixin, Base, WebhookPayloadMixin, table=True):
    __tablename__ = "services"
    __scope_prefix__ = "service"

    name: str = Field(max_length=255, unique=True, nullable=False)
    description: Optional[str] = Field(max_length=1000, nullable=True)
    price: SerializableDecimal = Field(sa_column=Column(DECIMAL(10, 2), nullable=False))
    currency: str = Field(max_length=3, default="UAH")
    is_active: bool = Field(default=True)
    category: Optional[str] = Field(max_length=100, nullable=True)

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "full",
            trigger_fields={"name", "description", "price", "currency", "is_active", "category"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "status",
            trigger_fields={"is_active"},
            fields={"id", "name", "is_active"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "price",
            trigger_fields={"price"},
            fields={"id", "name", "price"},
            stage=WebhookStage.BOTH,
        )
