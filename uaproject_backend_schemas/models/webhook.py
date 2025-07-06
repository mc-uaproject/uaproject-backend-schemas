from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlmodel import (
    JSON,
    BigInteger,
    Column,
    Enum,
    Float,
    ForeignKey,
    Index,
    Relationship,
)

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.types import SerializableHttpUrl
from uaproject_backend_schemas.models.schemas.webhook import (
    WebhookAuthType,
    WebhookPayloadTemplate,
    WebhookRetryPolicy,
    WebhookStatus,
    WebhookTrigger,
)

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User
    from uaproject_backend_schemas.models.webhook_log import WebhookLog


class Webhook(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "webhooks"
    __scope_prefix__ = "webhook"
    __table_args__ = (
        Index("ix_webhooks_user_id", "user_id"),
        Index("ix_webhooks_status", "status"),
    )

    # Main fields
    name: str = AwesomeField(description="Name of webhook for convenience")
    description: Optional[str] = AwesomeField(default=None, description="Description of webhook")
    endpoint: SerializableHttpUrl = AwesomeField(sa_column=Column(JSON, nullable=False))
    user_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True)
    )

    # Status and settings
    status: WebhookStatus = AwesomeField(
        sa_column=Column(
            Enum(WebhookStatus, native_enum=False),
            default=WebhookStatus.ACTIVE.value,
            server_default=WebhookStatus.ACTIVE.value,
        )
    )
    is_system: bool = AwesomeField(default=False, description="System webhook (cannot be deleted)")
    priority: int = AwesomeField(
        default=100, description="Priority of execution (lower = higher priority)"
    )

    # Triggers configuration
    triggers: List[WebhookTrigger] = AwesomeField(
        sa_column=Column(JSON, default=list), description="List of triggers for different models"
    )

    # Payload settings
    payload_config: WebhookPayloadTemplate = AwesomeField(
        sa_column=Column(JSON, default=dict), description="Payload configuration"
    )

    # Retry policy
    retry_policy: WebhookRetryPolicy = AwesomeField(
        sa_column=Column(JSON, default=dict), description="Retry policy"
    )

    # Authorization
    auth_type: Optional[WebhookAuthType] = AwesomeField(
        sa_column=Column(
            Enum(WebhookAuthType, native_enum=False),
            nullable=True,
        ),
        default=None,
        description="Authorization type: bearer, basic, api_key, hmac, oauth2, custom",
    )
    auth_config: Optional[Dict[str, Any]] = AwesomeField(
        sa_column=Column(JSON, default=None, nullable=True),
        description="Authorization configuration (encrypted)",
    )

    # Sending settings
    timeout: int = AwesomeField(default=30, description="Request timeout in seconds")
    follow_redirects: bool = AwesomeField(default=True, description="Follow redirects")
    verify_ssl: bool = AwesomeField(default=True, description="Verify SSL certificate")

    # Schedule (for periodic webhooks)
    schedule_cron: Optional[str] = AwesomeField(
        default=None, description="Cron expression for periodic runs"
    )
    schedule_timezone: Optional[str] = AwesomeField(
        default="UTC", description="Timezone for scheduling"
    )

    # Statistics
    last_triggered_at: Optional[datetime] = AwesomeField(default=None)
    last_success_at: Optional[datetime] = AwesomeField(default=None)
    last_error: Optional[str] = AwesomeField(default=None)
    last_error_at: Optional[datetime] = AwesomeField(default=None)
    last_response_status: Optional[int] = AwesomeField(default=None)
    last_response_time_ms: Optional[int] = AwesomeField(default=None)
    total_triggers: int = AwesomeField(default=0)
    success_triggers: int = AwesomeField(default=0)
    failed_triggers: int = AwesomeField(default=0)
    average_response_time_ms: Optional[float] = AwesomeField(
        sa_column=Column(Float, default=None, nullable=True)
    )

    # Metadata
    tags: Optional[List[str]] = AwesomeField(
        sa_column=Column(JSON, default=None), description="Tags for grouping"
    )
    webhook_metadata: Optional[Dict[str, Any]] = AwesomeField(
        sa_column=Column(JSON, default=None), description="Additional metadata"
    )

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="webhooks",
        sa_relationship_kwargs={"foreign_keys": "[Webhook.user_id]"},
    )
    logs: List["WebhookLog"] = Relationship(back_populates="webhook")
