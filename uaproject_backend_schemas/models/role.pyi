# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Role(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    permissions: List[Dict]
    weight: int
    users: Optional[List[User]]
    schemas: RoleSchemas
    scopes: RoleScopes
    filters: RoleFilters
    filter: type[RoleFilter]

class RoleSchemas:
    """Schemas for the Role model."""

class RoleScopes:
    """Scopes for the Role model."""

class RoleFilters:
    """Declarative filters for the Role model."""

class RoleFilter(BaseModel):
    """Pydantic-class for filtering the Role model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List] = None
    weight: Optional[int] = None
    min_weight: Optional[Any] = None
    max_weight: Optional[Any] = None
