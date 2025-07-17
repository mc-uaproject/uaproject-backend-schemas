# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Role(AwesomeModel):
    """Base role model."""

    created_at: datetime
    display_name: Optional[str]
    id: int
    name: str
    permissions: dict[str, bool]
    updated_at: datetime
    users: list[User]
    weight: int
    schemas: RoleSchemas
    filter: type[RoleFilter]
    sort: type[RoleSort]

class RoleSchemas:
    """Schemas for the Role model."""

    create: RoleSchemaCreate
    redis: RoleSchemaRedis
    response: RoleSchemaResponse
    update: RoleSchemaUpdate

class RoleSchemaCreate(AwesomeBaseModel):
    """create schema for Role model"""

    display_name: Optional[str]
    permissions: Optional[dict[str, bool]]
    name: Optional[str]
    weight: Optional[int]

class RoleSchemaRedis(AwesomeBaseModel):
    """redis schema for Role model"""

    display_name: Optional[str]
    permissions: Optional[dict[str, bool]]
    updated_at: Optional[datetime]
    id: Optional[int]
    users: Optional[list[User]]
    name: Optional[str]
    weight: Optional[int]
    created_at: datetime

class RoleSchemaResponse(AwesomeBaseModel):
    """response schema for Role model"""

    display_name: Optional[str]
    permissions: Optional[dict[str, bool]]
    updated_at: Optional[datetime]
    id: Optional[int]
    name: str
    weight: Optional[int]
    created_at: datetime

class RoleSchemaUpdate(AwesomeBaseModel):
    """update schema for Role model"""

    display_name: Optional[str]
    permissions: Optional[dict[str, bool]]
    name: Optional[str]
    weight: Optional[int]

class RoleFilter(BaseModel):
    """Pydantic-class for filtering the Role model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    weight: Optional[int] = None
    min_weight: Optional[int] = None
    max_weight: Optional[int] = None
    users_id: Optional[int] = None

class RoleSort(StrEnum):
    """Enum for sorting the Role model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
