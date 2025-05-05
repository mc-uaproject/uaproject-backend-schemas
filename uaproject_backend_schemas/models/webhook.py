from typing import TYPE_CHECKING, Dict, Optional

from sqlmodel import JSON, BigInteger, Column, Enum, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.types import SerializableHttpUrl
from uaproject_backend_schemas.models.schemas.webhook import WebhookStatus

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User


class Webhook(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "webhooks"
    __scope_prefix__ = "webhook"

    endpoint: SerializableHttpUrl = AwesomeField(sa_column=Column(JSON, nullable=False))
    user_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True)
    )

    status: WebhookStatus = AwesomeField(
        sa_column=Column(
            Enum(WebhookStatus, native_enum=False),
            default=WebhookStatus.ACTIVE.value,
            server_default=WebhookStatus.ACTIVE.value,
        )
    )

    webhook_scopes: Dict[str, bool] = AwesomeField(
        sa_column=Column(JSON, default=dict), alias=["scopes"]
    )
    authorization: Optional[str] = AwesomeField(sa_column=Column(JSON, default=None, nullable=True))

    user: Optional["User"] = Relationship(
        back_populates="webhooks",
        sa_relationship_kwargs={"foreign_keys": "[Webhook.user_id]"},
    )
