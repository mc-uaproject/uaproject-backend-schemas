import re
import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import model_validator
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, ForeignKey, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.users.payload import DiscordIdPayload, MinecraftNicknamePayload
from uaproject_backend_schemas.users.roles import Role, UserRoles
from uaproject_backend_schemas.webhooks.mixins import WebhookChangesMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.applications import Application
    from uaproject_backend_schemas.payments import Balance, Transaction
    from uaproject_backend_schemas.punishments import Punishment
    from uaproject_backend_schemas.webhooks.models import Webhook

__all__ = ["User", "Token"]


class User(
    Base,
    IDMixin,
    TimestampsMixin,
    WebhookChangesMixin,
    table=True,
):
    __tablename__ = "users"
    __scope_prefix__ = "user"

    model_config = {"arbitrary_types_allowed": True}

    discord_id: Optional[int] = Field(
        default=None, sa_column=Column(BigInteger(), index=True, unique=True)
    )
    minecraft_nickname: Optional[str] = Field(
        default=None, index=True, nullable=True, max_length=16
    )
    is_superuser: Optional[bool] = Field(default=False, nullable=True)
    biography: Optional[str] = Field(default=None, nullable=True)
    access: Optional[bool] = Field(default=False, nullable=True)

    roles: List["Role"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"secondary": UserRoles.__table__}
    )

    user_roles: List["UserRoles"] = Relationship(
       back_populates="user"
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

    @model_validator(mode="before")
    def validate_minecraft_nickname(cls, values):
        nickname = values.get("minecraft_nickname")
        if nickname is None:
            return values
        if not 3 <= len(nickname) <= 16:
            raise ValueError("Minecraft nickname must be between 3 and 16 characters.")
        if not re.match(r"^[a-zA-Z0-9_]+$", nickname):
            raise ValueError(
                "Minecraft nickname can only contain letters, numbers, and underscores."
            )
        return values

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "minecraft_nickname",
            trigger_fields={"minecraft_nickname"},
            fields=MinecraftNicknamePayload.model_construct(),
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "discord_id",
            trigger_fields={"discord_id"},
            fields=DiscordIdPayload.model_construct(),
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "superuser",
            trigger_fields={"is_superuser"},
            fields={"id", "discord_id", "minecraft_nickname", "is_superuser", "updated_at"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "access",
            trigger_fields={"access"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "full",
            trigger_fields={"discord_id", "minecraft_nickname", "is_superuser", "access"},
            stage=WebhookStage.AFTER,
        )


class Token(Base, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "user_tokens"

    token: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False, unique=True)

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False))
    user: "User" = Relationship(back_populates="token")


# class UserActivityLog(Base, IDMixin, TimestampsMixin):
#     __tablename__ = "user_activity_logs"

#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
#     activity_type: Mapped[ActivityType]
#     ip_address: Mapped[Optional[str]]
#     user_agent: Mapped[Optional[str]]
#     details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
#     performed_by_id: Mapped[Optional[int]] = mapped_column(
#         ForeignKey("users.id", ondelete="SET NULL")
#     )

#     # Relationships
#     user = Relationship(back_populates="activities")
