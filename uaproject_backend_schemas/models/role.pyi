# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Role(AwesomeModel):
    """Base role model."""

    updated_at: datetime
    id: int
    name: str
    display_name: Optional[str]
    permissions: List[Dict]
    weight: int
    users: Optional[List[User]]
    schemas: RoleSchemas
    scopes: RoleScopes
    filters: RoleFilters
    sorts: RoleSorts
    filter: type[RoleFilter]
    sort: type[RoleSort]

class RoleSchemas:
    """Schemas for the Role model."""

    create: RoleSchemaCreate
    update: RoleSchemaUpdate
    response: RoleSchemaResponse

class RoleSchemaCreate(AwesomeBaseModel):
    """create schema for Role model"""

    name: str
    display_name: Optional[str]
    permissions: List[Dict]
    weight: int
    users: Optional[List[User]]

class RoleSchemaUpdate(AwesomeBaseModel):
    """update schema for Role model"""

    name: str
    display_name: Optional[str]
    permissions: List[Dict]
    weight: int
    users: Optional[List[User]]

class RoleSchemaResponse(AwesomeBaseModel):
    """response schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    display_name: Optional[str]
    permissions: List[Dict]
    weight: int
    users: Optional[List[User]]

class RoleScopes:
    """Scopes for the Role model."""

class RoleFilters:
    """Declarative filters for the Role model."""

class RoleFilter(BaseModel):
    """Pydantic-class for filtering the Role model."""

class RoleSorts:
    """Declarative sorts for the Role model."""

class RoleSort(StrEnum):
    """Enum for sorting the Role model."""
