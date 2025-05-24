# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

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
    filters: PunishmentFilters
    filter: type[PunishmentFilter]

class PunishmentSchemas:
    """Schemas for the user model."""

    create: PunishmentSchemaCreate
    update: PunishmentSchemaUpdate
    response: PunishmentSchemaResponse

class PunishmentScopes:
    """Visibility scopes for the user model."""

    created: PunishmentScopeCreated
    status_changed: PunishmentScopeStatusChanged

class PunishmentFilters:
    """Declarative filters for the Punishment model."""

class PunishmentFilter(BaseModel):
    """Pydantic-class for filtering the Punishment model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    admin_id: Optional[int] = None
    min_admin_id: Optional[Any] = None
    max_admin_id: Optional[Any] = None
    type: Optional[PunishmentType] = None
    status: Optional[PunishmentStatus] = None
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    min_expires_at: Optional[Any] = None
    max_expires_at: Optional[Any] = None
    config_id: Optional[int] = None
    min_config_id: Optional[Any] = None
    max_config_id: Optional[Any] = None
    punishment_metadata: Optional[Dict] = None

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
