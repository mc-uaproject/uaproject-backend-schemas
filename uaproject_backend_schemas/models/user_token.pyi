# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Token(AwesomeModel):
    """Base token model."""

    id: int
    token: UUID
    updated_at: datetime
    user: User
    user_id: int
    schemas: TokenSchemas
    scopes: TokenScopes
    filter: type[TokenFilter]
    sort: type[TokenSort]

class TokenSchemas:
    """Schemas for the Token model."""

    create: TokenSchemaCreate
    update: TokenSchemaUpdate
    response: TokenSchemaResponse

class TokenSchemaCreate(AwesomeBaseModel):
    """create schema for Token model"""

    token: Optional[UUID]
    user_id: Optional[int]
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaCreate: ...

class TokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """create schema for Token model with permissions token.read"""

    token: Optional[UUID]
    user_id: Optional[int]
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaCreateWithPermissionsTokenRead: ...

class TokenSchemaCreateWithPermissionsTokenWrite(AwesomeBaseModel):
    """create schema for Token model with permissions token.write"""

    token: Optional[UUID]
    user_id: Optional[int]
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaCreateWithPermissionsTokenWrite: ...

class TokenSchemaUpdate(AwesomeBaseModel):
    """update schema for Token model"""

    token: Optional[UUID]
    user_id: Optional[int]
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaUpdate: ...

class TokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """update schema for Token model with permissions token.read"""

    token: Optional[UUID]
    user_id: Optional[int]
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaUpdateWithPermissionsTokenRead: ...

class TokenSchemaUpdateWithPermissionsTokenWrite(AwesomeBaseModel):
    """update schema for Token model with permissions token.write"""

    token: Optional[UUID]
    user_id: Optional[int]
    user: Optional[User]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaUpdateWithPermissionsTokenWrite: ...

class TokenSchemaResponse(AwesomeBaseModel):
    """response schema for Token model"""

    updated_at: datetime
    id: int
    token: UUID
    user_id: int
    user: User

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaResponse: ...

class TokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """response schema for Token model with permissions token.read"""

    updated_at: datetime
    id: int
    token: UUID
    user_id: int
    user: User

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaResponseWithPermissionsTokenRead: ...

class TokenSchemaResponseWithPermissionsTokenWrite(AwesomeBaseModel):
    """response schema for Token model with permissions token.write"""

    updated_at: datetime
    id: int
    token: UUID
    user_id: int
    user: User

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenSchemaResponseWithPermissionsTokenWrite: ...

class TokenScopes:
    """Scopes for the Token model."""

    full: TokenScopeFull

class TokenScopeFull(AwesomeBaseModel):
    """full schema for Token model"""

    updated_at: datetime
    id: int
    token: UUID
    user_id: int
    user: User

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenScopeFull: ...

class TokenScopeFullWithPermissionsTokenRead(AwesomeBaseModel):
    """full schema for Token model with permissions token.read"""

    updated_at: datetime
    id: int
    token: UUID
    user_id: int
    user: User

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenScopeFullWithPermissionsTokenRead: ...

class TokenScopeFullWithPermissionsTokenWrite(AwesomeBaseModel):
    """full schema for Token model with permissions token.write"""

    updated_at: datetime
    id: int
    token: UUID
    user_id: int
    user: User

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> TokenScopeFullWithPermissionsTokenWrite: ...

class TokenFilter(BaseModel):
    """Pydantic-class for filtering the Token model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    token: Optional[UUID] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None

class TokenSort(StrEnum):
    """Enum for sorting the Token model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
