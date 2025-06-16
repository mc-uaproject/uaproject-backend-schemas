# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Optional

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
    filters: PunishmentConfigFilters
    sorts: PunishmentConfigSorts
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

class PunishmentConfigFilters:
    """Declarative filters for the PunishmentConfig model."""

class PunishmentConfigFilter(BaseModel):
    """Pydantic-class for filtering the PunishmentConfig model."""

class PunishmentConfigSorts:
    """Declarative sorts for the PunishmentConfig model."""

class PunishmentConfigSort(StrEnum):
    """Enum for sorting the PunishmentConfig model."""
