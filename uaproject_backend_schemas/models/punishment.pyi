# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.punishment_config import PunishmentConfig
from uaproject_backend_schemas.models.schemas.punishment import PunishmentStatus, PunishmentType
from uaproject_backend_schemas.models.user import User

class Punishment(AwesomeModel):
    """Base punishment model."""

    admin: Optional[User]
    admin_id: Optional[int]
    config: Optional[PunishmentConfig]
    config_id: Optional[int]
    created_at: datetime
    expires_at: Optional[datetime]
    id: int
    punishment_metadata: Optional[dict[str, Any]]
    reason: Optional[str]
    status: PunishmentStatus
    type: PunishmentType
    updated_at: datetime
    user: Optional[User]
    user_id: int
    schemas: PunishmentSchemas
    filter: type[PunishmentFilter]
    sort: type[PunishmentSort]

class PunishmentSchemas:
    """Schemas for the Punishment model."""

    create: PunishmentSchemaCreate
    redis: PunishmentSchemaRedis
    response: PunishmentSchemaResponse
    update: PunishmentSchemaUpdate

class PunishmentSchemaCreate(AwesomeBaseModel):
    """create schema for Punishment model"""

    expires_at: Optional[datetime]
    status: Optional[PunishmentStatus]
    user_id: Optional[int]
    admin_id: Optional[int]
    reason: Optional[str]
    punishment_metadata: Optional[dict[str, Any]]
    type: Optional[PunishmentType]
    config_id: Optional[int]

class PunishmentSchemaRedis(AwesomeBaseModel):
    """redis schema for Punishment model"""

    expires_at: Optional[datetime]
    id: Optional[int]
    user: Optional[User]
    status: Optional[PunishmentStatus]
    config: Optional[PunishmentConfig]
    user_id: Optional[int]
    admin_id: Optional[int]
    reason: Optional[str]
    punishment_metadata: Optional[dict[str, Any]]
    admin: Optional[User]
    created_at: Optional[datetime]
    type: Optional[PunishmentType]
    updated_at: Optional[datetime]
    config_id: Optional[int]

class PunishmentSchemaResponse(AwesomeBaseModel):
    """response schema for Punishment model"""

    expires_at: Optional[datetime]
    id: Optional[int]
    status: PunishmentStatus
    user_id: int
    admin_id: Optional[int]
    reason: Optional[str]
    punishment_metadata: Optional[dict[str, Any]]
    created_at: Optional[datetime]
    type: PunishmentType
    updated_at: Optional[datetime]
    config_id: Optional[int]

class PunishmentSchemaUpdate(AwesomeBaseModel):
    """update schema for Punishment model"""

    expires_at: Optional[datetime]
    status: Optional[PunishmentStatus]
    user_id: Optional[int]
    admin_id: Optional[int]
    reason: Optional[str]
    punishment_metadata: Optional[dict[str, Any]]
    type: Optional[PunishmentType]
    config_id: Optional[int]

class PunishmentFilter(BaseModel):
    """Pydantic-class for filtering the Punishment model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    admin_id: Optional[int] = None
    min_admin_id: Optional[int] = None
    max_admin_id: Optional[int] = None
    type: Optional[PunishmentType] = None
    status: Optional[PunishmentStatus] = None
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    min_expires_at: Optional[datetime] = None
    max_expires_at: Optional[datetime] = None
    config_id: Optional[int] = None
    min_config_id: Optional[int] = None
    max_config_id: Optional[int] = None
    config_name: Optional[str] = None

class PunishmentSort(StrEnum):
    """Enum for sorting the Punishment model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
