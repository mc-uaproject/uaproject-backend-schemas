# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class UserRoles(AwesomeModel):
    """Base userroles model."""

    id: int
    role_id: int
    updated_at: datetime
    user_id: int
    schemas: UserRolesSchemas
    scopes: UserRolesScopes
    filter: type[UserRolesFilter]
    sort: type[UserRolesSort]

class UserRolesSchemas:
    """Schemas for the UserRoles model."""

    create: UserRolesSchemaCreate
    update: UserRolesSchemaUpdate
    response: UserRolesSchemaResponse

class UserRolesSchemaCreate(AwesomeBaseModel):
    """create schema for UserRoles model"""

    user_id: Optional[int]
    role_id: Optional[int]

class UserRolesSchemaUpdate(AwesomeBaseModel):
    """update schema for UserRoles model"""

    user_id: Optional[int]
    role_id: Optional[int]

class UserRolesSchemaResponse(AwesomeBaseModel):
    """response schema for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int

class UserRolesScopes:
    """Scopes for the UserRoles model."""

class UserRolesFilter(BaseModel):
    """Pydantic-class for filtering the UserRoles model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    role_id: Optional[int] = None
    min_role_id: Optional[Any] = None
    max_role_id: Optional[Any] = None

class UserRolesSort(StrEnum):
    """Enum for sorting the UserRoles model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
