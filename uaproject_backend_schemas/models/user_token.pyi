# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Literal
from uuid import UUID

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel, AwesomeField

class Token(AwesomeModel):
    """Base user model."""

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
    """create schema for Token model"""

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
    """create schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """create schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaCreateWithPermissionsTokenWrite
        | TokenSchemaCreateWithPermissionsTokenRead
        | TokenSchemaCreateWithPermissions
    ): ...

class TokenSchemaUpdate(AwesomeBaseModel):
    """update schema for Token model"""

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
    """update schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """update schema for Token model with permissions token.read"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaUpdateWithPermissionsTokenWrite
        | TokenSchemaUpdateWithPermissionsTokenRead
        | TokenSchemaUpdateWithPermissions
    ): ...

class TokenSchemaResponse(AwesomeBaseModel):
    """response schema for Token model"""

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
    """response schema for Token model with permissions token.write"""

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"])

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenSchemaResponseWithPermissionsTokenWrite
        | TokenSchemaResponseWithPermissionsTokenRead
        | TokenSchemaResponseWithPermissions
    ): ...

class TokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """response schema for Token model with permissions token.read"""

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
