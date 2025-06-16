from typing import TYPE_CHECKING, List, Optional

from sqlmodel import JSON, BigInteger, Column, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.ticket import Ticket
    from uaproject_backend_schemas.models.user import User


class TicketMessage(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    __tablename__ = "ticket_messages"
    __scope_prefix__ = "ticket_message"
    model_config = {"arbitrary_types_allowed": True}

    ticket_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("tickets.id"), nullable=False)
    )
    author_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )

    content: str = AwesomeField(max_length=4096, description="Message content (supports markdown)")
    attachments: Optional[List[str]] = AwesomeField(
        sa_column=Column(JSON, nullable=True, default=[]),
        default_factory=list,
        description="List of attachment URLs/paths",
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
                "attachments",
                "is_system_message",
                "edited_at",
                "created_at",
                "updated_at",
            ]
            relationships = {"author": "UserResponseSchema"}
            permissions = [".read"]

    class Scopes(AwesomeModel.Scopes):
        class TicketMessages(ScopeDefinition):
            trigger_fields = ["ticket_id"]
            fields = ["id", "ticket_id", "author_id", "content", "created_at"]
            permissions = [".read"]


if __name__ == "__main__":
    print(TicketMessage.schemas.list())
