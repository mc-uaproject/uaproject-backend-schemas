# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Role(AwesomeModel):
    """Base role model."""

    display_name: Optional[str]
    id: int
    name: str
    permissions: dict[str, bool]
    updated_at: datetime
    users: list[User]
    weight: int
    schemas: RoleSchemas
    scopes: RoleScopes
    filter: type[RoleFilter]
    sort: type[RoleSort]

class RoleSchemas:
    """Schemas for the Role model."""

    create: RoleSchemaCreate
    update: RoleSchemaUpdate
    response: RoleSchemaResponse

class RoleSchemaCreate(AwesomeBaseModel):
    """create schema for Role model"""

    name: Optional[str]
    display_name: Optional[str]
    permissions: Optional[dict[str, bool]]
    weight: Optional[int]
    users: Optional[list[User]]

class RoleSchemaUpdate(AwesomeBaseModel):
    """update schema for Role model"""

    name: Optional[str]
    display_name: Optional[str]
    permissions: Optional[dict[str, bool]]
    weight: Optional[int]
    users: Optional[list[User]]

class RoleSchemaResponse(AwesomeBaseModel):
    """response schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    display_name: Optional[str]
    permissions: dict[str, bool]
    weight: int
    users: list[User]

class RoleScopes:
    """Scopes for the Role model."""

class RoleFilter(BaseModel):
    """Pydantic-class for filtering the Role model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    weight: Optional[int] = None
    min_weight: Optional[Any] = None
    max_weight: Optional[Any] = None
    users_id: Optional[Any] = None

class RoleSort(StrEnum):
    """Enum for sorting the Role model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
