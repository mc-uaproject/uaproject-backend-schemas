# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Dict, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class PunishmentConfig(AwesomeModel):
    """Base user model."""

    schemas: PunishmentConfigSchemas
    scopes: PunishmentConfigScopes

class PunishmentConfigSchemas:
    """Schemas for the user model."""

    create: PunishmentConfigSchemaCreate
    update: PunishmentConfigSchemaUpdate
    response: PunishmentConfigSchemaResponse

class PunishmentConfigScopes:
    """Visibility scopes for the user model."""

    changed: PunishmentConfigScopeChanged

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
