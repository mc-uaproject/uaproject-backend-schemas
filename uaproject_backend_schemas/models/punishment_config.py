from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlmodel import JSON, Column, Index, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.punishment import Punishment


class PunishmentConfig(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "punishment_configs"
    __scope_prefix__ = "punishment_config"
    __table_args__ = (
        Index("ix_punishment_configs_name", "name"),
        Index("ix_punishment_configs_active", "is_active"),
    )

    name: str = AwesomeField(max_length=100)
    description: Optional[str] = AwesomeField(default=None)
    is_active: bool = AwesomeField(default=True)
    warn_threshold: int = AwesomeField(default=3)
    warn_decay_days: int = AwesomeField(default=30)
    config_data: Dict[str, Any] = AwesomeField(sa_column=Column(JSON, nullable=False, default={}))

    punishments: List["Punishment"] = Relationship(back_populates="config")
