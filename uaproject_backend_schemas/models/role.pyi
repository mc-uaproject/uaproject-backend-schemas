# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import List, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class Role(AwesomeModel):
    """Base user model."""

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
    """create schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]

class RoleSchemaUpdate(AwesomeBaseModel):
    """update schema for Role model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[str]

class RoleSchemaResponse(AwesomeBaseModel):
    """response schema for Role model"""

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
