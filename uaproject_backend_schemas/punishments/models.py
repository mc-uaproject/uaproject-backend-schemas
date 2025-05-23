from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlmodel import JSON, BigInteger, Column, DateTime, Enum, Field, ForeignKey, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.punishments.schemas import PunishmentStatus, PunishmentType
from uaproject_backend_schemas.webhooks.mixins import (
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
)
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User

__all__ = ["Punishment", "PunishmentConfig"]


class PunishmentConfig(
    TimestampsMixin,
    IDMixin,
    Base,
    WebhookChangesMixin,
    table=True,
):
    __tablename__ = "punishment_configs"
    __scope_prefix__ = "punishment_config"

    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    warn_threshold: int = Field(default=3)
    warn_decay_days: int = Field(default=30)
    config_data: Dict[str, Any] = Field(sa_column=Column(JSON, nullable=False, default={}))

    punishments: List["Punishment"] = Relationship(back_populates="config")

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "changed",
            trigger_fields={
                "name",
                "description",
                "is_active",
                "warn_threshold",
                "warn_decay_days",
                "config_data",
            },
            fields={
                "id",
                "name",
                "description",
                "is_active",
                "warn_threshold",
                "warn_decay_days",
            },
            stage=WebhookStage.BOTH,
        )


class Punishment(
    TimestampsMixin,
    IDMixin,
    Base,
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
    table=True,
):
    __tablename__ = "punishments"
    __scope_prefix__ = "punishment"

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False))
    admin_id: Optional[int] = Field(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True)
    )
    type: PunishmentType = Field(sa_column=Column(Enum(PunishmentType, native_enum=False)))
    status: PunishmentStatus = Field(
        sa_column=Column(
            Enum(PunishmentStatus, native_enum=False),
            default=PunishmentStatus.ACTIVE.value,
            server_default=PunishmentStatus.ACTIVE.value,
        )
    )
    reason: Optional[str] = Field(default=None)
    expires_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    config_id: Optional[int] = Field(
        sa_column=Column(BigInteger(), ForeignKey("punishment_configs.id"), nullable=True)
    )
    punishment_metadata: Optional[Dict[str, Any]] = Field(sa_column=Column(JSON, nullable=True))

    user: Optional["User"] = Relationship(
        back_populates="punishments",
        sa_relationship_kwargs={"foreign_keys": "[Punishment.user_id]"},
    )
    admin: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Punishment.admin_id]"},
    )
    config: Optional[PunishmentConfig] = Relationship(back_populates="punishments")

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "created",
            trigger_fields={
                "user_id",
                "admin_id",
                "type",
                "status",
                "reason",
                "expires_at",
                "config_id",
            },
            fields={"id", "user_id", "admin_id", "type", "status", "reason", "expires_at"},
            stage=WebhookStage.AFTER,
            relationships={
                "user": {"fields": ["id", "discord_id", "minecraft_nickname"]},
                "admin": {"fields": ["id", "discord_id", "minecraft_nickname"]},
                "config": {"fields": ["id", "name", "warn_threshold", "warn_decay_days"]},
            },
        )

        cls.register_scope(
            "status_changed",
            trigger_fields={"status"},
            fields={"id", "user_id", "admin_id", "type", "status", "reason", "punishment_metadata"},
            stage=WebhookStage.BOTH,
            relationships={
                "user": {"fields": ["id", "discord_id", "minecraft_nickname"]},
                "admin": {"fields": ["id", "discord_id", "minecraft_nickname"]},
            },
            temporal_fields=[
                {
                    "expires_at_field": "expires_at",
                    "status_field": "status",
                    "status_value": PunishmentStatus.EXPIRED.value,
                    "scope_name": "punishment.status_changed",
                }
            ],
        )
