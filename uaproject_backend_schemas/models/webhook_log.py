import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlmodel import (
    JSON,
    BigInteger,
    Column,
    Enum,
    ForeignKey,
    Index,
    Relationship,
    Text,
)

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.webhook import WebhookEvent, WebhookLogStatus

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.file import File
    from uaproject_backend_schemas.models.webhook import Webhook


class WebhookLog(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "webhook_logs"
    __scope_prefix__ = "webhook_log"
    __table_args__ = (
        Index("ix_webhook_logs_webhook_id", "webhook_id"),
        Index("ix_webhook_logs_status", "status"),
        Index("ix_webhook_logs_request_payload_file_id", "request_payload_file_id"),
        Index("ix_webhook_logs_response_body_file_id", "response_body_file_id"),
    )

    event_id: uuid.UUID = AwesomeField(
        default_factory=uuid.uuid4,
        description="Unique identifier for the event",
        sa_column=Column(unique=True, nullable=False),
    )

    webhook_id: int = AwesomeField(
        sa_column=Column(
            BigInteger(), ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False
        )
    )

    status: WebhookLogStatus = AwesomeField(
        sa_column=Column(
            Enum(WebhookLogStatus, native_enum=False),
            default=WebhookLogStatus.PENDING.value,
            server_default=WebhookLogStatus.PENDING.value,
            nullable=False,
        )
    )

    triggered_by_event: WebhookEvent = AwesomeField(
        sa_column=Column(Enum(WebhookEvent, native_enum=False), nullable=False)
    )

    attempt: int = AwesomeField(default=1, description="Attempt number (for retries)")

    request_headers: Dict[str, Any] = AwesomeField(
        sa_column=Column(JSON, nullable=False), description="Request headers sent to endpoint"
    )
    request_payload: Optional[Dict[str, Any]] = AwesomeField(
        sa_column=Column(JSON, nullable=True),
        description="Request payload sent to endpoint (if small)",
    )
    request_payload_file_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("files.id"), nullable=True),
        description="ID of the file in MinIO for large request payload",
    )

    response_status_code: Optional[int] = AwesomeField(
        default=None, description="HTTP status code received from the endpoint"
    )
    response_headers: Optional[Dict[str, Any]] = AwesomeField(
        sa_column=Column(JSON), default=None, description="Response headers received from endpoint"
    )
    response_body: Optional[str] = AwesomeField(
        sa_column=Column(Text),
        default=None,
        description="Response body received (if small and not binary)",
    )
    response_body_file_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("files.id"), nullable=True),
        description="ID of the file in MinIO for large or binary response body",
    )

    execution_duration_ms: Optional[int] = AwesomeField(
        default=None, description="Total execution time in milliseconds"
    )

    # Relationship to the main webhook
    webhook: "Webhook" = Relationship(
        back_populates="logs",
        sa_relationship_kwargs={"foreign_keys": "[WebhookLog.webhook_id]"},
    )

    # Relationships to File model for large payloads/bodies
    request_payload_file: Optional["File"] = Relationship(
        back_populates="webhook_logs_as_request",
        sa_relationship_kwargs={
            "foreign_keys": "[WebhookLog.request_payload_file_id]",
        },
    )
    response_body_file: Optional["File"] = Relationship(
        back_populates="webhook_logs_as_response",
        sa_relationship_kwargs={
            "foreign_keys": "[WebhookLog.response_body_file_id]",
        },
    )
