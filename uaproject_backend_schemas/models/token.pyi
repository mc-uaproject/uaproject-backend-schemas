# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Token(AwesomeModel):
    """Base token model."""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    created_at: datetime
    user: Optional[User]
    schemas: TokenSchemas
    scopes: TokenScopes
    filters: TokenFilters
    sorts: TokenSorts
    filter: type[TokenFilter]
    sort: type[TokenSort]

class TokenSchemas:
    """Schemas for the Token model."""

    create: TokenSchemaCreate
    update: TokenSchemaUpdate
    response: TokenSchemaResponse

class TokenSchemaCreate(AwesomeBaseModel):
    """create schema for Token model"""

    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaCreate: ...

class TokenSchemaCreateWithPermissionsTokenWrite(AwesomeBaseModel):
    """create schema for Token model with permissions token.write"""

    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaCreateWithPermissionsTokenWrite: ...

class TokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """create schema for Token model with permissions token.read"""

    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaCreateWithPermissionsTokenRead: ...

class TokenSchemaUpdate(AwesomeBaseModel):
    """update schema for Token model"""

    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaUpdate: ...

class TokenSchemaUpdateWithPermissionsTokenWrite(AwesomeBaseModel):
    """update schema for Token model with permissions token.write"""

    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaUpdateWithPermissionsTokenWrite: ...

class TokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """update schema for Token model with permissions token.read"""

    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaUpdateWithPermissionsTokenRead: ...

class TokenSchemaResponse(AwesomeBaseModel):
    """response schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaResponse: ...

class TokenSchemaResponseWithPermissionsTokenWrite(AwesomeBaseModel):
    """response schema for Token model with permissions token.write"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaResponseWithPermissionsTokenWrite: ...

class TokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """response schema for Token model with permissions token.read"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenSchemaResponseWithPermissionsTokenRead: ...

class TokenScopes:
    """Scopes for the Token model."""

    full: TokenScopeFull

class TokenScopeFull(AwesomeBaseModel):
    """full schema for Token model"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenScopeFull: ...

class TokenScopeFullWithPermissionsTokenWrite(AwesomeBaseModel):
    """full schema for Token model with permissions token.write"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenScopeFullWithPermissionsTokenWrite: ...

class TokenScopeFullWithPermissionsTokenRead(AwesomeBaseModel):
    """full schema for Token model with permissions token.read"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> TokenScopeFullWithPermissionsTokenRead: ...

class TokenFilters:
    """Declarative filters for the Token model."""

class TokenFilter(BaseModel):
    """Pydantic-class for filtering the Token model."""

class TokenSorts:
    """Declarative sorts for the Token model."""

class TokenSort(StrEnum):
    """Enum for sorting the Token model."""
