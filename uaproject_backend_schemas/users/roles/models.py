from typing import TYPE_CHECKING, List, Optional

from sqlmodel import JSON, BigInteger, Column, Field, ForeignKey, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.webhooks.mixins import (
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
)
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User

__all__ = ["Role", "UserRoles"]


class UserRoles(
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
    TimestampsMixin,
    IDMixin,
    Base,
    table=True,
):
    __tablename__ = "user_roles"
    __scope_prefix__ = "user_role"

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), primary_key=True))
    role_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("roles.id"), primary_key=True))

    user: Optional["User"] = Relationship(
        back_populates="user_roles",
        sa_relationship_kwargs={"foreign_keys": "[UserRoles.user_id]"},
    )
    role: Optional["Role"] = Relationship(
        back_populates="user_roles",
        sa_relationship_kwargs={"foreign_keys": "[UserRoles.role_id]"},
    )

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "created",
            trigger_fields={"user_id", "role_id"},
            fields={"id", "user_id", "role_id"},
            stage=WebhookStage.AFTER,
            relationships={
                "user": {"fields": ["id", "discord_id", "minecraft_nickname"]},
                "role": {"fields": ["id", "name", "display_name"]},
            },
        )

        cls.register_scope(
            "deleted",
            trigger_fields={"user_id", "role_id"},
            fields={"id", "user_id", "role_id"},
            stage=WebhookStage.BEFORE,
            relationships={
                "user": {"fields": ["id", "discord_id", "minecraft_nickname"]},
                "role": {"fields": ["id", "name", "display_name"]},
            },
        )


class Role(
    WebhookChangesMixin,
    TimestampsMixin,
    IDMixin,
    Base,
    table=True,
):
    __tablename__ = "roles"
    __scope_prefix__ = "role"

    name: str = Field(unique=True, index=True)
    display_name: str | None = Field(default=None, nullable=True)
    permissions: List[str] = Field(sa_column=Column(JSON))
    weight: int = Field(default=0, index=True)

    users: List["User"] = Relationship(
        back_populates="roles", sa_relationship_kwargs={"secondary": UserRoles.__table__}
    )

    user_roles: List["UserRoles"] = Relationship(
       back_populates="role"
   )

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "created",
            trigger_fields={"name", "display_name", "permissions", "weight"},
            fields={"id", "name", "display_name", "permissions", "weight"},
            stage=WebhookStage.AFTER,
        )

        cls.register_scope(
            "updated",
            trigger_fields={"name", "display_name", "permissions", "weight"},
            fields={"id", "name", "display_name", "permissions", "weight"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "permissions",
            trigger_fields={"permissions"},
            fields={"id", "name", "display_name", "permissions"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "weight",
            trigger_fields={"weight"},
            fields={"id", "name", "display_name", "weight"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "display_name",
            trigger_fields={"display_name"},
            fields={"id", "name", "display_name"},
            stage=WebhookStage.BOTH,
        )
