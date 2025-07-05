from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import field_serializer, field_validator
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

    # Custom serializers for complex fields
    @field_serializer("triggers")
    def serialize_triggers(self, value: List[WebhookTrigger]) -> List[Dict[str, Any]]:
        """Serialize triggers to dict for JSON storage"""
        if not value:
            return []
        return [trigger.model_dump() if hasattr(trigger, 'model_dump') else trigger for trigger in value]
    
    @field_validator("triggers", mode="before")
    @classmethod
    def validate_triggers(cls, value) -> List[WebhookTrigger]:
        """Validate and convert triggers from dict/list to WebhookTrigger objects"""
        if not value:
            return []
        
        result = []
        for item in value:
            if isinstance(item, WebhookTrigger):
                result.append(item)
            elif isinstance(item, dict):
                result.append(WebhookTrigger(**item))
            else:
                # Try to convert to dict first
                try:
                    if hasattr(item, 'model_dump'):
                        result.append(WebhookTrigger(**item.model_dump()))
                    else:
                        result.append(WebhookTrigger(**item))
                except Exception:
                    # Skip invalid items
                    continue
        return result
    
    @field_serializer("payload_config")
    def serialize_payload_config(self, value: WebhookPayloadTemplate) -> Dict[str, Any]:
        """Serialize payload_config to dict for JSON storage"""
        if not value:
            return {}
        return value.model_dump() if hasattr(value, 'model_dump') else value
    
    @field_validator("payload_config", mode="before")
    @classmethod
    def validate_payload_config(cls, value) -> WebhookPayloadTemplate:
        """Validate and convert payload_config from dict to WebhookPayloadTemplate"""
        if not value:
            return WebhookPayloadTemplate()
        
        if isinstance(value, WebhookPayloadTemplate):
            return value
        elif isinstance(value, dict):
            return WebhookPayloadTemplate(**value)
        else:
            try:
                if hasattr(value, 'model_dump'):
                    return WebhookPayloadTemplate(**value.model_dump())
                else:
                    return WebhookPayloadTemplate(**value)
            except Exception:
                return WebhookPayloadTemplate()
    
    @field_serializer("retry_policy")
    def serialize_retry_policy(self, value: WebhookRetryPolicy) -> Dict[str, Any]:
        """Serialize retry_policy to dict for JSON storage"""
        if not value:
            return {}
        return value.model_dump() if hasattr(value, 'model_dump') else value
    
    @field_validator("retry_policy", mode="before") 
    @classmethod
    def validate_retry_policy(cls, value) -> WebhookRetryPolicy:
        """Validate and convert retry_policy from dict to WebhookRetryPolicy"""
        if not value:
            return WebhookRetryPolicy()
        
        if isinstance(value, WebhookRetryPolicy):
            return value
        elif isinstance(value, dict):
            return WebhookRetryPolicy(**value)
        else:
            try:
                if hasattr(value, 'model_dump'):
                    return WebhookRetryPolicy(**value.model_dump())
                else:
                    return WebhookRetryPolicy(**value)
            except Exception:
                return WebhookRetryPolicy()

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="webhooks",
        sa_relationship_kwargs={"foreign_keys": "[Webhook.user_id]"},
    )
    logs: List["WebhookLog"] = Relationship(back_populates="webhook")
