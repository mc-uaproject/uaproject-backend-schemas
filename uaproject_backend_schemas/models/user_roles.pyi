# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class UserRoles(AwesomeModel):
    """Base userroles model."""

    created_at: datetime
    id: int
    role_id: int
    updated_at: datetime
    user_id: int
    schemas: UserRolesSchemas
    filter: type[UserRolesFilter]
    sort: type[UserRolesSort]

class UserRolesSchemas:
    """Schemas for the UserRoles model."""

    create: UserRolesSchemaCreate
    redis: UserRolesSchemaRedis
    response: UserRolesSchemaResponse
    update: UserRolesSchemaUpdate

class UserRolesSchemaCreate(AwesomeBaseModel):
    """create schema for UserRoles model"""

    user_id: Optional[int]
    role_id: Optional[int]

class UserRolesSchemaRedis(AwesomeBaseModel):
    """redis schema for UserRoles model"""

    user_id: Optional[int]
    updated_at: Optional[datetime]
    role_id: Optional[int]
    id: Optional[int]
    created_at: datetime

class UserRolesSchemaResponse(AwesomeBaseModel):
    """response schema for UserRoles model"""

    user_id: int
    updated_at: Optional[datetime]
    role_id: int
    id: Optional[int]
    created_at: datetime

class UserRolesSchemaUpdate(AwesomeBaseModel):
    """update schema for UserRoles model"""

    user_id: Optional[int]
    role_id: Optional[int]

class UserRolesFilter(BaseModel):
    """Pydantic-class for filtering the UserRoles model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    role_id: Optional[int] = None
    min_role_id: Optional[int] = None
    max_role_id: Optional[int] = None

class UserRolesSort(StrEnum):
    """Enum for sorting the UserRoles model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
