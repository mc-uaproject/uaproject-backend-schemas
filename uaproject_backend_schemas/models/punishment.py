from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlmodel import JSON, BigInteger, Column, DateTime, Enum, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.punishment_config import PunishmentConfig
    from uaproject_backend_schemas.models.user import User


class PunishmentType(StrEnum):
    WARN = "warn"
    MUTE = "mute"
    BAN = "ban"
    KICK = "kick"
    RESTRICTION = "restriction"


class PunishmentStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class Punishment(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "punishments"
    __scope_prefix__ = "punishment"
    model_config = {"arbitrary_types_allowed": True}

    user_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )
    admin_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True)
    )
    type: PunishmentType = AwesomeField(sa_column=Column(Enum(PunishmentType, native_enum=False)))
    status: PunishmentStatus = AwesomeField(
        sa_column=Column(
            Enum(PunishmentStatus, native_enum=False),
            default=PunishmentStatus.ACTIVE.value,
            server_default=PunishmentStatus.ACTIVE.value,
        )
    )
    reason: Optional[str] = AwesomeField(default=None)
    expires_at: Optional[datetime] = AwesomeField(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    config_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("punishment_configs.id"), nullable=True)
    )
    punishment_metadata: Optional[Dict[str, Any]] = AwesomeField(
        sa_column=Column(JSON, nullable=True)
    )

    user: Optional["User"] = Relationship(
        back_populates="punishments",
        sa_relationship_kwargs={"foreign_keys": "[Punishment.user_id]"},
    )
    admin: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Punishment.admin_id]"},
    )
    config: Optional["PunishmentConfig"] = Relationship(back_populates="punishments")

    user: "User" = Relationship(back_populates="punishments")

    class Scopes(AwesomeModel.Scopes):
        class Created(ScopeDefinition):
            trigger_fields = ["created_at"]
            fields = ["id", "user_id", "created_at"]
            permissions = ["punishment.read"]

        class StatusChanged(ScopeDefinition):
            trigger_fields = ["status"]
            permissions = ["punishment.read"]
