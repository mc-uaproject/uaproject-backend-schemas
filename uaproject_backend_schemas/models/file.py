from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Relationship,
    String,
)

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.news import News
    from uaproject_backend_schemas.models.service import Service
    from uaproject_backend_schemas.models.ticket_message import TicketMessage
    from uaproject_backend_schemas.models.user import User
    from uaproject_backend_schemas.models.webhook_log import WebhookLog


class File(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "files"
    __scope_prefix__ = "file"

    # Storage info
    bucket: str = AwesomeField(
        max_length=100,
        nullable=False,
        description="MinIO bucket name",
    )
    path: str = AwesomeField(
        max_length=500,
        nullable=False,
        unique=True,
        description="Full path in bucket (with date prefix)",
    )

    # Metadata
    original_name: str = AwesomeField(
        max_length=255,
        nullable=False,
        description="Original filename",
    )
    content_type: str = AwesomeField(
        max_length=100,
        nullable=False,
        description="MIME type",
    )
    size: int = AwesomeField(
        sa_column=Column(BigInteger, nullable=False),
        description="File size in bytes",
    )
    checksum: Optional[str] = AwesomeField(
        max_length=64,
        nullable=True,
        description="SHA256 checksum",
    )
    checksum_type: str = AwesomeField(
        max_length=20,
        default="sha256",
        description="Checksum algorithm",
    )

    # Relations
    user_id: int = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("users.id"), nullable=False),
        description="User who uploaded the file",
    )
    model_name: Optional[str] = AwesomeField(
        max_length=50,
        nullable=True,
        description="Related model name (e.g., 'news', 'ticket_message')",
    )
    model_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, nullable=True),
        description="Related model ID",
    )

    # Status
    status: str = AwesomeField(
        sa_column=Column(String(20), default="pending"),
        description="File status: pending, uploaded, failed, deleted",
    )

    # Additional timestamps
    uploaded_at: Optional[datetime] = AwesomeField(
        sa_column=Column(DateTime, nullable=True),
        description="When file upload was confirmed",
    )

    # Foreign keys for specific models
    ticket_message_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("ticket_messages.id"), nullable=True),
        description="Related ticket message ID (if file is ticket attachment)",
    )
    news_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("news.id"), nullable=True),
        description="Related news ID (if file is news cover)",
    )
    service_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("services.id"), nullable=True),
        description="Related service ID (if file is service icon)",
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="files")
    ticket_message: Optional["TicketMessage"] = Relationship(back_populates="attachment_files")
    news: Optional["News"] = Relationship(back_populates="images")
    service: Optional["Service"] = Relationship(back_populates="icon_file")

    webhook_logs_as_request: List["WebhookLog"] = Relationship(
        back_populates="request_payload_file",
        sa_relationship_kwargs={
            "foreign_keys": "[WebhookLog.request_payload_file_id]",
        },
    )
    webhook_logs_as_response: List["WebhookLog"] = Relationship(
        back_populates="response_body_file",
        sa_relationship_kwargs={
            "foreign_keys": "[WebhookLog.response_body_file_id]",
        },
    )

    __table_args__ = (
        Index("idx_model_lookup", "model_name", "model_id"),
        Index("idx_user_files", "user_id", "updated_at"),
        Index("idx_file_status", "status", "updated_at"),
    )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "uploaded_at", "status"]
            optional = True
            permissions = [".write"]

        class Update(SchemaDefinition):
            fields = ["status", "checksum"]
            optional = True
            permissions = [".write"]

        class Response(SchemaDefinition):
            permissions = [".read"]

        class RequestUpload(SchemaDefinition):
            fields = ["model_name", "model_id", "original_name", "content_type", "size"]
            permissions = [".write"]
