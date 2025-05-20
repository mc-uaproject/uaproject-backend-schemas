# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class UserRoles(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int
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
    """Create schema for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int

class UserRolesSchemaUpdate(AwesomeBaseModel):
    """Update schema for UserRoles model"""

    updated_at: datetime
    id: int
    user_id: int
    role_id: int

class UserRolesSchemaResponse(AwesomeBaseModel):
    """Response schema for UserRoles model"""

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
