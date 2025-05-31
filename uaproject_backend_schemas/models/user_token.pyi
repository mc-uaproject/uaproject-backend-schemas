# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Token(AwesomeModel):
    """Base user model."""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]
    schemas: TokenSchemas
    scopes: TokenScopes
    filters: TokenFilters
    filter: type[TokenFilter]

class TokenSchemas:
    """Schemas for the Token model."""

class TokenScopes:
    """Scopes for the Token model."""

    full: TokenScopeFull

class TokenScopeFull(AwesomeBaseModel):
    """full schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(required_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenScopeFull: ...

class TokenScopeFullWithPermissionsTokenWrite(AwesomeBaseModel):
    """full schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(required_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenScopeFullWithPermissionsTokenWrite: ...

class TokenScopeFullWithPermissionsTokenRead(AwesomeBaseModel):
    """full schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(required_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenScopeFullWithPermissionsTokenRead: ...

class TokenFilters:
    """Declarative filters for the Token model."""

class TokenFilter(BaseModel):
    """Pydantic-class for filtering the Token model."""

    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    token: Optional[UUID] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
