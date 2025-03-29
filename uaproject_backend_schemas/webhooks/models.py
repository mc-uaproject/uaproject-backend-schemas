import logging
from typing import TYPE_CHECKING, Dict, Optional

from sqlalchemy import JSON, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlmodel import Field, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.schemas import SerializableHttpUrl
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStatus

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User

__all__ = ["Webhook"]
logger = logging.getLogger(__name__)


class Webhook(Base, IDMixin, TimestampsMixin, WebhookPayloadMixin, table=True):
    __tablename__ = "webhooks"
    __scope_prefix__ = "webhook"

    endpoint: SerializableHttpUrl = Field(sa_column=Column(JSON, nullable=False))
    user_id: int = Field(foreign_key="users.id", nullable=True)

    status: WebhookStatus = Field(
        sa_column=Column(
            SQLAlchemyEnum(WebhookStatus, native_enum=False),
            default=WebhookStatus.ACTIVE.value,
            server_default=WebhookStatus.ACTIVE.value,
        )
    )

    scopes: Dict[str, bool] = Field(sa_column=Column(JSON, default=dict))
    authorization: str | None = Field(sa_column=Column(JSON, default=None, nullable=True))

    user: Optional["User"] = Relationship(
        back_populates="webhooks",
        sa_relationship_kwargs={"foreign_keys": "[Webhook.user_id]"},
    )

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "status",
            trigger_fields={"status"},
            fields={"id", "endpoint", "status"},
            stage="both",
        )

        cls.register_scope(
            "endpoint",
            trigger_fields={"endpoint"},
            fields={"id", "endpoint", "status"},
            stage="both",
        )

        cls.register_scope(
            "scopes",
            trigger_fields={"scopes"},
            fields={"id", "endpoint", "status", "scopes"},
            stage="both",
        )

        cls.register_scope(
            "authorization",
            trigger_fields={"authorization"},
            fields={"id", "endpoint", "status", "scopes", "authorization"},
            stage="both",
        )
