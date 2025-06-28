# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.punishment import Punishment

class PunishmentConfig(AwesomeModel):
    """Base punishmentconfig model."""

    config_data: dict[str, Any]
    created_at: datetime
    description: Optional[str]
    id: int
    is_active: bool
    name: str
    punishments: list[Punishment]
    updated_at: datetime
    warn_decay_days: int
    warn_threshold: int
    schemas: PunishmentConfigSchemas
    filter: type[PunishmentConfigFilter]
    sort: type[PunishmentConfigSort]

class PunishmentConfigSchemas:
    """Schemas for the PunishmentConfig model."""

    create: PunishmentConfigSchemaCreate
    redis: PunishmentConfigSchemaRedis
    response: PunishmentConfigSchemaResponse
    update: PunishmentConfigSchemaUpdate

class PunishmentConfigSchemaCreate(AwesomeBaseModel):
    """create schema for PunishmentConfig model"""

    config_data: Optional[dict[str, Any]]
    is_active: Optional[bool]
    warn_threshold: Optional[int]
    warn_decay_days: Optional[int]
    description: Optional[str]
    name: Optional[str]

class PunishmentConfigSchemaRedis(AwesomeBaseModel):
    """redis schema for PunishmentConfig model"""

    config_data: Optional[dict[str, Any]]
    created_at: Optional[datetime]
    is_active: Optional[bool]
    punishments: Optional[list[Punishment]]
    warn_threshold: Optional[int]
    warn_decay_days: Optional[int]
    updated_at: Optional[datetime]
    description: Optional[str]
    id: Optional[int]
    name: Optional[str]

class PunishmentConfigSchemaResponse(AwesomeBaseModel):
    """response schema for PunishmentConfig model"""

    config_data: dict[str, Any]
    created_at: Optional[datetime]
    is_active: Optional[bool]
    warn_threshold: Optional[int]
    warn_decay_days: Optional[int]
    updated_at: Optional[datetime]
    description: Optional[str]
    id: Optional[int]
    name: str

class PunishmentConfigSchemaUpdate(AwesomeBaseModel):
    """update schema for PunishmentConfig model"""

    config_data: Optional[dict[str, Any]]
    is_active: Optional[bool]
    warn_threshold: Optional[int]
    warn_decay_days: Optional[int]
    description: Optional[str]
    name: Optional[str]

class PunishmentConfigFilter(BaseModel):
    """Pydantic-class for filtering the PunishmentConfig model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    warn_threshold: Optional[int] = None
    min_warn_threshold: Optional[Any] = None
    max_warn_threshold: Optional[Any] = None
    warn_decay_days: Optional[int] = None
    min_warn_decay_days: Optional[Any] = None
    max_warn_decay_days: Optional[Any] = None
    punishments_id: Optional[Any] = None

class PunishmentConfigSort(StrEnum):
    """Enum for sorting the PunishmentConfig model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
