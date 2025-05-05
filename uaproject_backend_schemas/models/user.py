import re
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import model_validator
from sqlmodel import BigInteger, Column, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition
from uaproject_backend_schemas.models.user_token import Token

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.application import Application
    from uaproject_backend_schemas.models.balance import Balance
    from uaproject_backend_schemas.models.punishment import Punishment
    from uaproject_backend_schemas.models.role import Role
    from uaproject_backend_schemas.models.transaction import Transaction
    from uaproject_backend_schemas.models.webhook import Webhook


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class User(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    __tablename__ = "users"
    __scope_prefix__ = "user"
    model_config = {"arbitrary_types_allowed": True}

    discord_id: Optional[int] = AwesomeField(
        default=None, sa_column=Column(BigInteger(), index=True, unique=True)
    )
    minecraft_nickname: Optional[str] = AwesomeField(
        default=None, index=True, nullable=True, max_length=16
    )
    is_superuser: Optional[bool] = AwesomeField(default=False, nullable=True)
    biography: Optional[str] = AwesomeField(default=None, nullable=True, max_length=2048)
    access: Optional[bool] = AwesomeField(default=False, nullable=True)

    roles: List["Role"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"secondary": "user_roles"}
    )
    token: Optional["Token"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
            "lazy": "joined",
        },
    )
    punishments: List["Punishment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Punishment.user_id]"}
    )
    balance: Optional["Balance"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False, "lazy": "joined"}
    )
    application: Optional["Application"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False, "lazy": "joined"}
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

    class Scopes(AwesomeModel.Scopes):
        class MinecraftNickname(ScopeDefinition):
            trigger_fields = ["minecraft_nickname"]
            fields = ["id", "minecraft_nickname"]

        class DiscordId(ScopeDefinition):
            trigger_fields = ["discord_id"]
            fields = ["id", "discord_id"]

        class Superuser(ScopeDefinition):
            trigger_fields = ["is_superuser"]
            fields = ["id", "discord_id", "minecraft_nickname", "is_superuser", "updated_at"]

        class Access(ScopeDefinition):
            trigger_fields = ["access"]
            fields = ["id", "access"]

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

if __name__ == "__main__":
    print(User.scopes.list())
