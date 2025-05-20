# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import List, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Role(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]
    users: Optional[List[User]]
    schemas: RoleSchemas
    scopes: RoleScopes

class RoleSchemas:
    """Schemas for the user model."""

    create: RoleSchemaCreate
    update: RoleSchemaUpdate
    response: RoleSchemaResponse

class RoleScopes:
    """Visibility scopes for the user model."""

    full: RoleScopeFull

class RoleSchemaCreate(AwesomeBaseModel):
    """Create schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]

class RoleSchemaUpdate(AwesomeBaseModel):
    """Update schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]

class RoleSchemaResponse(AwesomeBaseModel):
    """Response schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]

class RoleScopeFull(AwesomeBaseModel):
    """full visibility scope for Role model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]
