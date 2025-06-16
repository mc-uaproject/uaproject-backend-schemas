# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Dict, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.punishment_config import PunishmentConfig
from uaproject_backend_schemas.models.schemas.punishment import PunishmentStatus, PunishmentType
from uaproject_backend_schemas.models.user import User

class Punishment(AwesomeModel):
    """Base punishment model."""

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
    created_at: datetime
    user: Optional[User]
    admin: Optional[User]
    config: Optional[PunishmentConfig]
    schemas: PunishmentSchemas
    scopes: PunishmentScopes
    filters: PunishmentFilters
    sorts: PunishmentSorts
    filter: type[PunishmentFilter]
    sort: type[PunishmentSort]

class PunishmentSchemas:
    """Schemas for the Punishment model."""

    create: PunishmentSchemaCreate
    update: PunishmentSchemaUpdate
    response: PunishmentSchemaResponse

class PunishmentSchemaCreate(AwesomeBaseModel):
    """create schema for Punishment model"""

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

class PunishmentSchemaUpdate(AwesomeBaseModel):
    """update schema for Punishment model"""

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
    user: Optional[User]
    admin: Optional[User]
    config: Optional[PunishmentConfig]

class PunishmentScopes:
    """Scopes for the Punishment model."""

    created: PunishmentScopeCreated
    status_changed: PunishmentScopeStatusChanged

class PunishmentScopeCreated(AwesomeBaseModel):
    """created schema for Punishment model"""

    id: int
    user_id: int
    created_at: datetime

class PunishmentScopeStatusChanged(AwesomeBaseModel):
    """status_changed schema for Punishment model"""

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

class PunishmentFilters:
    """Declarative filters for the Punishment model."""

class PunishmentFilter(BaseModel):
    """Pydantic-class for filtering the Punishment model."""

class PunishmentSorts:
    """Declarative sorts for the Punishment model."""

class PunishmentSort(StrEnum):
    """Enum for sorting the Punishment model."""
