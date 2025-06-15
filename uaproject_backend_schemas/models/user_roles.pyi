# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class UserRoles(AwesomeModel):
    """Base userroles model."""

    updated_at: datetime
    user_id: int
    role_id: int
    schemas: UserRolesSchemas
    scopes: UserRolesScopes
    filters: UserRolesFilters
    sorts: UserRolesSorts
    filter: type[UserRolesFilter]
    sort: type[UserRolesSort]

class UserRolesSchemas:
    """Schemas for the UserRoles model."""

    create: UserRolesSchemaCreate
    update: UserRolesSchemaUpdate
    response: UserRolesSchemaResponse

class UserRolesSchemaCreate(AwesomeBaseModel):
    """create schema for UserRoles model"""

    user_id: int
    role_id: int

class UserRolesSchemaUpdate(AwesomeBaseModel):
    """update schema for UserRoles model"""

    user_id: int
    role_id: int

class UserRolesSchemaResponse(AwesomeBaseModel):
    """response schema for UserRoles model"""

    updated_at: datetime
    user_id: int
    role_id: int

class UserRolesScopes:
    """Scopes for the UserRoles model."""

class UserRolesFilters:
    """Declarative filters for the UserRoles model."""

class UserRolesFilter(BaseModel):
    """Pydantic-class for filtering the UserRoles model."""

class UserRolesSorts:
    """Declarative sorts for the UserRoles model."""

class UserRolesSort(StrEnum):
    """Enum for sorting the UserRoles model."""
