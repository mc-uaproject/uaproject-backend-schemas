from typing import TYPE_CHECKING, List, Optional

from sqlmodel import JSON, BigInteger, Column, ForeignKey, Index, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.file import File
    from uaproject_backend_schemas.models.ticket import Ticket
    from uaproject_backend_schemas.models.user import User


class TicketMessage(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "ticket_messages"
    __scope_prefix__ = "ticket_message"
    __table_args__ = (
        Index("ix_ticket_messages_ticket_updated", "ticket_id", "updated_at"),
        Index("ix_ticket_messages_author_id", "author_id"),
        Index("ix_ticket_messages_system", "is_system_message"),
    )

    ticket_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("tickets.id"), nullable=False)
    )
    author_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )

    content: str = AwesomeField(max_length=4096, description="Message content (supports markdown)")
    # MinIO file attachments (replacing old attachments field)
    attachment_file_ids: Optional[List[int]] = AwesomeField(
        sa_column=Column(JSON, nullable=True, default=[]),
        default_factory=list,
        description="List of File IDs for attachments",
    )

    is_system_message: bool = AwesomeField(
        default=False,
        description="Whether this is a system-generated message (e.g., status changes)",
    )
    edited_at: Optional[str] = AwesomeField(
        default=None, description="When message was last edited"
    )

    # Relationships
    ticket: Optional["Ticket"] = Relationship(back_populates="messages")
    author: Optional["User"] = Relationship(
        back_populates="ticket_messages",
        sa_relationship_kwargs={"foreign_keys": "[TicketMessage.author_id]", "uselist": False},
    )
    attachment_files: List["File"] = Relationship(back_populates="ticket_message")

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = [
                "id",
                "created_at",
                "updated_at",
                "author_id",
                "is_system_message",
                "edited_at",
            ]
            optional = True
            permissions = [".write"]

        class Update(SchemaDefinition):
            fields = ["content"]
            optional = True
            permissions = [".write.self"]

        class Response(SchemaDefinition):
            permissions = [".read"]

        class ResponseWithAuthor(SchemaDefinition):
            fields = [
                "id",
                "ticket_id",
                "author_id",
                "content",
                "attachment_file_ids",
                "is_system_message",
                "edited_at",
                "created_at",
                "updated_at",
            ]
            relationships = {"author": "UserResponseSchema"}
            permissions = [".read"]
