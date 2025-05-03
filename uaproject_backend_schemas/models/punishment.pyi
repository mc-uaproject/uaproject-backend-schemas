# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Dict, Optional

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel
from uaproject_backend_schemas.models.punishment import PunishmentStatus, PunishmentType

class Punishment(AwesomeModel):
    """Base user model."""

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
    """create schema for Punishment model"""

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
    """update schema for Punishment model"""

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
    """response schema for Punishment model"""

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
