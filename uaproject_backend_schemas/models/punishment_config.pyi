# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.punishment import Punishment

class PunishmentConfig(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
    punishments: Optional[List[Punishment]]
    schemas: PunishmentConfigSchemas
    scopes: PunishmentConfigScopes
    filters: PunishmentConfigFilters
    filter: type[PunishmentConfigFilter]

class PunishmentConfigSchemas:
    """Schemas for the user model."""

    create: PunishmentConfigSchemaCreate
    update: PunishmentConfigSchemaUpdate
    response: PunishmentConfigSchemaResponse

class PunishmentConfigScopes:
    """Visibility scopes for the user model."""

    changed: PunishmentConfigScopeChanged

class PunishmentConfigFilters:
    """Declarative filters for the PunishmentConfig model."""

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
    config_data: Optional[Dict] = None

class PunishmentConfigSchemaCreate(AwesomeBaseModel):
    """Create schema for PunishmentConfig model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict

class PunishmentConfigSchemaUpdate(AwesomeBaseModel):
    """Update schema for PunishmentConfig model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict

class PunishmentConfigSchemaResponse(AwesomeBaseModel):
    """Response schema for PunishmentConfig model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict

class PunishmentConfigScopeChanged(AwesomeBaseModel):
    """changed visibility scope for PunishmentConfig model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    warn_threshold: int
    warn_decay_days: int
    config_data: Dict
