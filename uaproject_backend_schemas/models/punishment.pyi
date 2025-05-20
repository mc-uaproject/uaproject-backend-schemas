# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Dict, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.punishment_config import PunishmentConfig
from uaproject_backend_schemas.models.schemas.punishment import PunishmentStatus, PunishmentType
from uaproject_backend_schemas.models.user import User

class Punishment(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    user_id: int
    admin_id: Optional[int]
    type: PunishmentType
    status: PunishmentStatus
    reason: Optional[str]
    expires_at: Optional[datetime]
    config_id: Optional[int]
    punishment_metadata: Optional[Dict]
    user: Optional[User]
    admin: Optional[User]
    config: Optional[PunishmentConfig]
    schemas: PunishmentSchemas
    scopes: PunishmentScopes

class PunishmentSchemas:
    """Schemas for the user model."""

    create: PunishmentSchemaCreate
    update: PunishmentSchemaUpdate
    response: PunishmentSchemaResponse

class PunishmentScopes:
    """Visibility scopes for the user model."""

    created: PunishmentScopeCreated
    status_changed: PunishmentScopeStatusChanged

class PunishmentSchemaCreate(AwesomeBaseModel):
    """Create schema for Punishment model"""

    updated_at: datetime
    id: int
    user_id: int
    admin_id: Optional[int]
    type: PunishmentType
    status: PunishmentStatus
    reason: Optional[str]
    expires_at: Optional[datetime]
    config_id: Optional[int]
    punishment_metadata: Optional[Dict]

class PunishmentSchemaUpdate(AwesomeBaseModel):
    """Update schema for Punishment model"""

    updated_at: datetime
    id: int
    user_id: int
    admin_id: Optional[int]
    type: PunishmentType
    status: PunishmentStatus
    reason: Optional[str]
    expires_at: Optional[datetime]
    config_id: Optional[int]
    punishment_metadata: Optional[Dict]

class PunishmentSchemaResponse(AwesomeBaseModel):
    """Response schema for Punishment model"""

    updated_at: datetime
    id: int
    user_id: int
    admin_id: Optional[int]
    type: PunishmentType
    status: PunishmentStatus
    reason: Optional[str]
    expires_at: Optional[datetime]
    config_id: Optional[int]
    punishment_metadata: Optional[Dict]

class PunishmentScopeCreated(AwesomeBaseModel):
    """created visibility scope for Punishment model"""

    id: int
    user_id: int

class PunishmentScopeStatusChanged(AwesomeBaseModel):
    """status_changed visibility scope for Punishment model"""

    updated_at: datetime
    id: int
    user_id: int
    admin_id: Optional[int]
    type: PunishmentType
    status: PunishmentStatus
    reason: Optional[str]
    expires_at: Optional[datetime]
    config_id: Optional[int]
    punishment_metadata: Optional[Dict]
