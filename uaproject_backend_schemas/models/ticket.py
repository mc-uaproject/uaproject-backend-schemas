from typing import TYPE_CHECKING, List, Optional

from sqlmodel import ARRAY, BigInteger, Column, Enum, ForeignKey, Relationship, select

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition
from uaproject_backend_schemas.models.schemas.ticket import TicketPriority, TicketStatus

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.ticket_message import TicketMessage
    from uaproject_backend_schemas.models.user import User


class Ticket(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    __tablename__ = "tickets"
    __scope_prefix__ = "ticket"
    model_config = {"arbitrary_types_allowed": True}

    title: str = AwesomeField(max_length=255)
    description: str = AwesomeField(max_length=4096)

    author_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )
    assigned_to_id: Optional[int] = AwesomeField(
        default=None, sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True)
    )
    added_user_ids: List[int] = AwesomeField(
        sa_column=Column(ARRAY(BigInteger()), nullable=False, default=[], server_default="{}")
    )

    status: TicketStatus = AwesomeField(
        sa_column=Column(
            Enum(TicketStatus, native_enum=False),
            default=TicketStatus.OPEN.value,
            server_default=TicketStatus.OPEN.value,
        )
    )
    priority: TicketPriority = AwesomeField(
        sa_column=Column(
            Enum(TicketPriority, native_enum=False),
            default=TicketPriority.MEDIUM.value,
            server_default=TicketPriority.MEDIUM.value,
        )
    )

    author: Optional["User"] = Relationship(
        back_populates="authored_tickets",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.author_id]", "uselist": False},
    )
    assigned_to: Optional["User"] = Relationship(
        back_populates="assigned_tickets",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to_id]", "uselist": False},
    )
    messages: List["TicketMessage"] = Relationship(
        back_populates="ticket", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def get_added_users(self, session) -> List["User"]:
        """Get users that were added to this ticket by their IDs."""
        if not self.added_user_ids:
            return []

        from uaproject_backend_schemas.models.user import User

        return session.exec(select(User).where(User.id.in_(self.added_user_ids))).all()

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "assigned_to_id", "added_user_ids"]
            optional = True
            permissions = [".write"]

        class Update(SchemaDefinition):
            fields = ["title", "description"]
            optional = True
            permissions = [".write.self"]

        class UpdateAssign(SchemaDefinition):
            fields = ["assigned_to_id", "added_user_ids", "status", "priority"]
            optional = True
            permissions = [".admin"]

        class Response(SchemaDefinition):
            permissions = [".read.other"]

        class ResponseSelf(SchemaDefinition):
            permissions = [".read.self"]

    class Scopes(AwesomeModel.Scopes):
        class Status(ScopeDefinition):
            trigger_fields = ["status"]
            fields = ["id", "author_id", "assigned_to_id", "status"]
            permissions = ["read"]

        class Priority(ScopeDefinition):
            trigger_fields = ["priority"]
            fields = ["id", "priority"]
            permissions = ["read"]

        class Assignment(ScopeDefinition):
            trigger_fields = ["assigned_to_id"]
            fields = ["id", "author_id", "assigned_to_id"]
            permissions = ["read"]


if __name__ == "__main__":
    print(Ticket.schemas.list())
    print(Ticket.sort)
