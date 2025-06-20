# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.punishment import Punishment

class PunishmentConfig(AwesomeModel):
    """Base punishmentconfig model."""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
    created_at: datetime
    punishments: Optional[List[Punishment]]
    schemas: PunishmentConfigSchemas
    scopes: PunishmentConfigScopes
    filter: type[PunishmentConfigFilter]
    sort: type[PunishmentConfigSort]

class PunishmentConfigSchemas:
    """Schemas for the PunishmentConfig model."""

    create: PunishmentConfigSchemaCreate
    update: PunishmentConfigSchemaUpdate
    response: PunishmentConfigSchemaResponse

class PunishmentConfigSchemaCreate(AwesomeBaseModel):
    """create schema for PunishmentConfig model"""

    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
    punishments: Optional[List[Punishment]]

class PunishmentConfigSchemaUpdate(AwesomeBaseModel):
    """update schema for PunishmentConfig model"""

    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
    punishments: Optional[List[Punishment]]

class PunishmentConfigSchemaResponse(AwesomeBaseModel):
    """response schema for PunishmentConfig model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
    punishments: Optional[List[Punishment]]

class PunishmentConfigScopes:
    """Scopes for the PunishmentConfig model."""

    changed: PunishmentConfigScopeChanged

class PunishmentConfigScopeChanged(AwesomeBaseModel):
    """changed schema for PunishmentConfig model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
    punishments: Optional[List[Punishment]]

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
