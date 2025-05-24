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
    """Schemas for the user model."""

    create: TokenSchemaCreate
    update: TokenSchemaUpdate
    response: TokenSchemaResponse

class TokenScopes:
    """Visibility scopes for the user model."""

    full: TokenScopeFull

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

class TokenSchemaCreate(AwesomeBaseModel):
    """Create schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissions(AwesomeBaseModel):
    """create schema for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """Create schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissionsTokenWrite(AwesomeBaseModel):
    """Create schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaUpdate(AwesomeBaseModel):
    """Update schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissions(AwesomeBaseModel):
    """update schema for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """Update schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissionsTokenWrite(AwesomeBaseModel):
    """Update schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaResponse(AwesomeBaseModel):
    """Response schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissions(AwesomeBaseModel):
    """response schema for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """Response schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissionsTokenWrite(AwesomeBaseModel):
    """Response schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenScopeFull(AwesomeBaseModel):
    """full visibility scope for Token model"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int

class TokenScopeFullWithPermissions(AwesomeBaseModel):
    """full visibility scope for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int

class TokenScopeFullWithPermissionsTokenRead(AwesomeBaseModel):
    """full visibility scope for Token model with permissions token.read"""

    token: UUID

class TokenScopeFullWithPermissionsTokenWrite(AwesomeBaseModel):
    """full visibility scope for Token model with permissions token.write"""

    token: UUID

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> (
        TokenScopeFullWithPermissionsTokenRead
        | TokenScopeFullWithPermissionsTokenWrite
        | TokenScopeFullWithPermissions
    ): ...
