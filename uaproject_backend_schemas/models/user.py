import re
from typing import TYPE_CHECKING, Dict, List, Optional

from pydantic import computed_field, field_validator
from sqlmodel import BigInteger, Column, Index, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.models.role import Role
from uaproject_backend_schemas.models.user_token import UserToken

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.application import Application
    from uaproject_backend_schemas.models.balance import Balance
    from uaproject_backend_schemas.models.claim import Claim
    from uaproject_backend_schemas.models.file import File
    from uaproject_backend_schemas.models.news import News
    from uaproject_backend_schemas.models.punishment import Punishment
    from uaproject_backend_schemas.models.purchased_item import PurchasedItem
    from uaproject_backend_schemas.models.session_token import SessionToken
    from uaproject_backend_schemas.models.ticket import Ticket
    from uaproject_backend_schemas.models.ticket_message import TicketMessage
    from uaproject_backend_schemas.models.transaction import Transaction
    from uaproject_backend_schemas.models.webhook import Webhook


class User(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "users"
    __scope_prefix__ = "user"
    __table_args__ = (Index("ix_users_superuser", "is_superuser"),)

    discord_id: Optional[int] = AwesomeField(
        default=None, sa_column=Column(BigInteger(), index=True, unique=True)
    )
    minecraft_nickname: Optional[str] = AwesomeField(
        default=None,
        index=True,
        nullable=True,
        max_length=16,
        min_length=3,
        unique=True,
        write_permissions=[".write.nickname"],
    )
    is_superuser: Optional[bool] = AwesomeField(
        default=False, nullable=True, read_permissions=[".admin"], write_permissions=[".admin"]
    )
    biography: Optional[str] = AwesomeField(default=None, nullable=True, max_length=2048)

    roles: List[Role] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"secondary": "user_roles"},
    )
    token: Optional["UserToken"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
        },
    )
    punishments: List["Punishment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Punishment.user_id]"}
    )
    balance: Optional["Balance"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    application: Optional["Application"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    transactions: List["Transaction"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Transaction.user_id]"}
    )
    received_transactions: List["Transaction"] = Relationship(
        back_populates="recipient",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.recipient_id]"},
    )
    webhooks: List["Webhook"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Webhook.user_id]"}
    )
    claims_as_claimant: List["Claim"] = Relationship(
        back_populates="claimants", sa_relationship_kwargs={"secondary": "claim_claimant_link"}
    )
    claims_as_defendant: List["Claim"] = Relationship(
        back_populates="defendants", sa_relationship_kwargs={"secondary": "claim_defendant_link"}
    )
    news: List["News"] = Relationship(
        back_populates="author", sa_relationship_kwargs={"foreign_keys": "[News.author_id]"}
    )
    authored_tickets: List["Ticket"] = Relationship(
        back_populates="author", sa_relationship_kwargs={"foreign_keys": "[Ticket.author_id]"}
    )
    assigned_tickets: List["Ticket"] = Relationship(
        back_populates="assigned_to",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to_id]"},
    )
    ticket_messages: List["TicketMessage"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"foreign_keys": "[TicketMessage.author_id]"},
    )
    # MinIO files uploaded by user
    files: List["File"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[File.user_id]"}
    )
    purchased_items: List["PurchasedItem"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[PurchasedItem.user_id]"}
    )
    sessions: List["SessionToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[SessionToken.user_id]"}
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
                "roles",
            ]
            permissions = [".read.other"]

    @field_validator("minecraft_nickname", mode="before")
    @classmethod
    def validate_nick(cls, value: str) -> str:
        """Validate Minecraft nickname."""
        if value is None:
            return value
        if not isinstance(value, str):
            msg = "minecraftnickname must be a string"
            raise TypeError(msg)
        if not re.fullmatch(r"[A-Za-z0-9]+", value):
            msg = "Minecraft nickname can only contain letters, numbers, and underscores."
            raise ValueError(msg)
        return value

    @computed_field(return_type=Dict[str, bool])
    @property
    def permissions(self) -> Dict[str, bool]:
        """Computed permissions with safe role access."""
        user_permissions = {}

        # Safe access to roles - check if roles are loaded
        try:
            if not hasattr(self, "roles") or self.roles is None:
                return user_permissions

            # Check if roles is actually loaded (not a lazy relationship)
            roles = self.roles
            if not isinstance(roles, list):
                return user_permissions

            sorted_roles = sorted(roles, key=lambda r: r.weight, reverse=False)
            for role in sorted_roles:
                if hasattr(role, "permissions") and role.permissions:
                    for user_permission_key, user_permission_value in role.permissions.items():
                        user_permissions[user_permission_key] = user_permission_value
        except Exception:
            # If any error occurs during role access, return empty permissions
            pass

        return user_permissions
