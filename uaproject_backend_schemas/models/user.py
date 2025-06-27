import re
from typing import TYPE_CHECKING, Dict, List, Optional

from pydantic import computed_field, model_validator
from sqlmodel import BigInteger, Column, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.models.role import Role
from uaproject_backend_schemas.models.user_token import Token

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.application import Application
    from uaproject_backend_schemas.models.balance import Balance
    from uaproject_backend_schemas.models.claim import Claim
    from uaproject_backend_schemas.models.file import File
    from uaproject_backend_schemas.models.news import News
    from uaproject_backend_schemas.models.punishment import Punishment
    from uaproject_backend_schemas.models.purchased_item import PurchasedItem
    from uaproject_backend_schemas.models.ticket import Ticket
    from uaproject_backend_schemas.models.ticket_message import TicketMessage
    from uaproject_backend_schemas.models.transaction import Transaction
    from uaproject_backend_schemas.models.webhook import Webhook


class User(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "users"
    __scope_prefix__ = "user"

    discord_id: Optional[int] = AwesomeField(
        default=None, sa_column=Column(BigInteger(), index=True, unique=True)
    )
    minecraft_nickname: Optional[str] = AwesomeField(
        default=None,
        index=True,
        nullable=True,
        max_length=16,
        unique=True,
        write_permissions=[".write.nickname"],
    )
    is_superuser: Optional[bool] = AwesomeField(
        default=False, nullable=True, read_permissions=[".admin"], write_permissions=[".admin"]
    )
    biography: Optional[str] = AwesomeField(default=None, nullable=True, max_length=2048)

    roles: List[Role] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"secondary": "user_roles", "lazy": "selectin"},
    )
    token: Optional["Token"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
            "lazy": "joined",
        },
    )
    punishments: List["Punishment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Punishment.user_id]", "lazy": "subquery"},
    )
    balance: Optional["Balance"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False, "lazy": "joined"}
    )
    application: Optional["Application"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False, "lazy": "joined"}
    )
    transactions: List["Transaction"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.user_id]", "lazy": "subquery"},
    )
    received_transactions: List["Transaction"] = Relationship(
        back_populates="recipient",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.recipient_id]", "lazy": "subquery"},
    )
    webhooks: List["Webhook"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Webhook.user_id]", "lazy": "selectin"},
    )
    claims_as_claimant: List["Claim"] = Relationship(
        back_populates="claimants",
        sa_relationship_kwargs={"secondary": "claim_claimant_link", "lazy": "selectin"},
    )
    claims_as_defendant: List["Claim"] = Relationship(
        back_populates="defendants",
        sa_relationship_kwargs={"secondary": "claim_defendant_link", "lazy": "selectin"},
    )
    news: List["News"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"foreign_keys": "[News.author_id]", "lazy": "selectin"},
    )
    authored_tickets: List["Ticket"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.author_id]", "lazy": "selectin"},
    )
    assigned_tickets: List["Ticket"] = Relationship(
        back_populates="assigned_to",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to_id]", "lazy": "selectin"},
    )
    ticket_messages: List["TicketMessage"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"foreign_keys": "[TicketMessage.author_id]", "lazy": "selectin"},
    )
    # MinIO files uploaded by user
    files: List["File"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[File.user_id]", "lazy": "selectin"},
    )
    purchased_items: List["PurchasedItem"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[PurchasedItem.user_id]", "lazy": "selectin"},
    )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "is_superuser", "access"]
            optional = True
            permissions = [".write"]

        class Update(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "is_superuser", "access"]
            optional = True
            permissions = [".write"]

        class UpdateAdmin(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at"]
            optional = True
            permissions = [".admin"]

        class Response(SchemaDefinition):
            fields = [
                "id",
                "updated_at",
                "created_at",
                "discord_id",
                "minecraft_nickname",
                "is_superuser",
                "biography",
                "access",
                "roles",
            ]
            permissions = [".read.other"]

    @model_validator(mode="before")
    def validate_fields(cls, values: Optional[dict[str, str]]) -> Optional[dict[str, str]]:
        if minecraft_nickname := values.get("minecraft_nickname", None):
            if not 3 <= len(minecraft_nickname) <= 16:
                raise ValueError("Minecraft nickname must be between 3 and 16 characters.")
            if not re.match(r"^[a-zA-Z0-9_]+$", minecraft_nickname):
                raise ValueError(
                    "Minecraft nickname can only contain letters, numbers, and underscores."
                )

        if biography := values.get("biography", None):
            if len(biography) > 2048:
                raise ValueError("Biography must be less than 2048 characters.")

        return values

    @computed_field(return_type=Dict[str, bool])
    @property
    def permissions(self) -> Dict[str, bool]:
        """Computed permissions with caching for performance."""
        user_permissions = {}

        sorted_roles = sorted(self.roles, key=lambda r: r.weight, reverse=False)
        for role in sorted_roles:
            for user_permission_key, user_permission_value in role.permissions.items():
                user_permissions[user_permission_key] = user_permission_value

        return user_permissions
