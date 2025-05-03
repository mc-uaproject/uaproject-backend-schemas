# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel

class UserRoles(AwesomeModel):
    """Base user model."""

    schemas: UserRolesSchemas
    scopes: UserRolesScopes

class UserRolesSchemas:
    """Schemas for the user model."""

    create: UserRolesSchemaCreate
    update: UserRolesSchemaUpdate
    response: UserRolesSchemaResponse

class UserRolesScopes:
    """Visibility scopes for the user model."""

    full: UserRolesScopeFull

class UserRolesSchemaCreate(AwesomeBaseModel):
    """create schema for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int

class UserRolesSchemaUpdate(AwesomeBaseModel):
    """update schema for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int

class UserRolesSchemaResponse(AwesomeBaseModel):
    """response schema for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int

class UserRolesScopeFull(AwesomeBaseModel):
    """full visibility scope for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int
