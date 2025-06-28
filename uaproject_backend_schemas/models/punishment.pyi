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

    status: Optional[PunishmentStatus]
    admin_id: Optional[int]
    user_id: Optional[int]
    config_id: Optional[int]
    expires_at: Optional[datetime]
    punishment_metadata: Optional[dict[str, Any]]
    type: Optional[PunishmentType]
    reason: Optional[str]

class PunishmentSchemaRedis(AwesomeBaseModel):
    """redis schema for Punishment model"""

    status: Optional[PunishmentStatus]
    user: Optional[User]
    admin: Optional[User]
    admin_id: Optional[int]
    config: Optional[PunishmentConfig]
    user_id: Optional[int]
    config_id: Optional[int]
    expires_at: Optional[datetime]
    punishment_metadata: Optional[dict[str, Any]]
    updated_at: Optional[datetime]
    type: Optional[PunishmentType]
    id: Optional[int]
    created_at: Optional[datetime]
    reason: Optional[str]

class PunishmentSchemaResponse(AwesomeBaseModel):
    """response schema for Punishment model"""

    status: PunishmentStatus
    admin_id: Optional[int]
    user_id: int
    config_id: Optional[int]
    expires_at: Optional[datetime]
    punishment_metadata: Optional[dict[str, Any]]
    updated_at: Optional[datetime]
    type: PunishmentType
    id: Optional[int]
    created_at: Optional[datetime]
    reason: Optional[str]

class PunishmentSchemaUpdate(AwesomeBaseModel):
    """update schema for Punishment model"""

    status: Optional[PunishmentStatus]
    admin_id: Optional[int]
    user_id: Optional[int]
    config_id: Optional[int]
    expires_at: Optional[datetime]
    punishment_metadata: Optional[dict[str, Any]]
    type: Optional[PunishmentType]
    reason: Optional[str]

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
    config_name: Optional[Any] = None

class PunishmentSort(StrEnum):
    """Enum for sorting the Punishment model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
