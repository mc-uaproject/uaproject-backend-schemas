import re
import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import model_validator
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, Relationship
from webhooks.mixins import WebhookPayloadMixin
from webhooks.schemas import WebhookStage

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.users.roles.models import Role, UserRoles

if TYPE_CHECKING:
    from uaproject_backend_schemas.applications import Application
    from uaproject_backend_schemas.payments import Balance, Transaction

__all__ = ["User", "Token"]


class User(Base, IDMixin, TimestampsMixin, WebhookPayloadMixin, table=True):
    __tablename__ = "users"
    __scope_prefix__ = "user"

    model_config = {"arbitrary_types_allowed": True}

    discord_id: Optional[int] = Field(default=None, sa_column=Column(BigInteger(), index=True))
    minecraft_nickname: Optional[str] = Field(
        default=None, index=True, nullable=True, max_length=16
    )
    is_superuser: Optional[bool] = Field(default=False, nullable=True)

    roles: List["Role"] = Relationship(sa_relationship_kwargs={"secondary": UserRoles})

    token: Optional["Token"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
            "lazy": "joined",
        },
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
            fields={"id", "discord_id", "minecraft_nickname", "updated_at"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "discord_id",
            trigger_fields={"discord_id"},
            fields={"id", "discord_id", "minecraft_nickname", "updated_at"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "superuser",
            trigger_fields={"is_superuser"},
            fields={"id", "discord_id", "minecraft_nickname", "is_superuser", "updated_at"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "full",
            trigger_fields={"discord_id", "minecraft_nickname", "is_superuser"},
            stage=WebhookStage.AFTER,
        )


class Token(Base, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "user_tokens"

    token: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False, unique=True)

    user_id: int = Field(foreign_key="users.id", nullable=False)
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
