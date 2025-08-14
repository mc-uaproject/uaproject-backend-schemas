# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class UserToken(AwesomeModel):
    """Base usertoken model."""

    created_at: datetime
    id: int
    token: UUID
    updated_at: datetime
    user: User
    user_id: int
    schemas: UserTokenSchemas
    filter: type[UserTokenFilter]
    sort: type[UserTokenSort]

class UserTokenSchemas:
    """Schemas for the UserToken model."""

    create: UserTokenSchemaCreate
    redis: UserTokenSchemaRedis
    response: UserTokenSchemaResponse
    update: UserTokenSchemaUpdate

class UserTokenSchemaCreate(AwesomeBaseModel):
    """create schema for UserToken model"""

    user_id: Optional[int]
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaCreate: ...

class UserTokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """create schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaCreateWithPermissionsTokenRead: ...

class UserTokenSchemaCreateWithPermissionsTokenWrite(AwesomeBaseModel):
    """create schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaCreateWithPermissionsTokenWrite: ...

class UserTokenSchemaRedis(AwesomeBaseModel):
    """redis schema for UserToken model"""

    user: Optional[User]
    user_id: Optional[int]
    token: Optional[UUID]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaRedis: ...

class UserTokenSchemaRedisWithPermissionsTokenRead(AwesomeBaseModel):
    """redis schema for UserToken model with permissions token.read"""

    user: Optional[User]
    user_id: int
    token: Optional[UUID]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaRedisWithPermissionsTokenRead: ...

class UserTokenSchemaRedisWithPermissionsTokenWrite(AwesomeBaseModel):
    """redis schema for UserToken model with permissions token.write"""

    user: Optional[User]
    user_id: int
    token: Optional[UUID]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaRedisWithPermissionsTokenWrite: ...

class UserTokenSchemaResponse(AwesomeBaseModel):
    """response schema for UserToken model"""

    user_id: int
    token: Optional[UUID]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaResponse: ...

class UserTokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """response schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaResponseWithPermissionsTokenRead: ...

class UserTokenSchemaResponseWithPermissionsTokenWrite(AwesomeBaseModel):
    """response schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaResponseWithPermissionsTokenWrite: ...

class UserTokenSchemaUpdate(AwesomeBaseModel):
    """update schema for UserToken model"""

    user_id: Optional[int]
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaUpdate: ...

class UserTokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """update schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaUpdateWithPermissionsTokenRead: ...

class UserTokenSchemaUpdateWithPermissionsTokenWrite(AwesomeBaseModel):
    """update schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.read", "token.write"]]
    ) -> UserTokenSchemaUpdateWithPermissionsTokenWrite: ...

class UserTokenFilter(BaseModel):
    """Pydantic-class for filtering the UserToken model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    token: Optional[UUID] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None

class UserTokenSort(StrEnum):
    """Enum for sorting the UserToken model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
