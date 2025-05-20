# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

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

class TokenSchemas:
    """Schemas for the user model."""

    create: TokenSchemaCreate
    update: TokenSchemaUpdate
    response: TokenSchemaResponse

class TokenScopes:
    """Visibility scopes for the user model."""

    full: TokenScopeFull

class TokenSchemaCreate(AwesomeBaseModel):
    """Create schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissions(AwesomeBaseModel):
    """create schema for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissionsTokenWrite(AwesomeBaseModel):
    """Create schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """Create schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaUpdate(AwesomeBaseModel):
    """Update schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissions(AwesomeBaseModel):
    """update schema for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissionsTokenWrite(AwesomeBaseModel):
    """Update schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """Update schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaResponse(AwesomeBaseModel):
    """Response schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissions(AwesomeBaseModel):
    """response schema for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])
    user_id: int

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissionsTokenWrite(AwesomeBaseModel):
    """Response schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """Response schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissionsTokenRead
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

class TokenScopeFullWithPermissionsTokenWrite(AwesomeBaseModel):
    """full visibility scope for Token model with permissions token.write"""

    token: UUID

class TokenScopeFullWithPermissionsTokenRead(AwesomeBaseModel):
    """full visibility scope for Token model with permissions token.read"""

    token: UUID

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenScopeFullWithPermissionsTokenWrite
        | TokenScopeFullWithPermissionsTokenRead
        | TokenScopeFullWithPermissions
    ): ...
