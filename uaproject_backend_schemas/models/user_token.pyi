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
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaCreate: ...

class UserTokenSchemaCreateWithPermissionsTokenWrite(AwesomeBaseModel):
    """create schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaCreateWithPermissionsTokenWrite: ...

class UserTokenSchemaCreateWithPermissionsTokenRead(AwesomeBaseModel):
    """create schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaCreateWithPermissionsTokenRead: ...

class UserTokenSchemaRedis(AwesomeBaseModel):
    """redis schema for UserToken model"""

    user_id: Optional[int]
    token: Optional[UUID]
    updated_at: Optional[datetime]
    user: Optional[User]
    id: Optional[int]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaRedis: ...

class UserTokenSchemaRedisWithPermissionsTokenWrite(AwesomeBaseModel):
    """redis schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]
    updated_at: Optional[datetime]
    user: Optional[User]
    id: Optional[int]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaRedisWithPermissionsTokenWrite: ...

class UserTokenSchemaRedisWithPermissionsTokenRead(AwesomeBaseModel):
    """redis schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]
    updated_at: Optional[datetime]
    user: Optional[User]
    id: Optional[int]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaRedisWithPermissionsTokenRead: ...

class UserTokenSchemaResponse(AwesomeBaseModel):
    """response schema for UserToken model"""

    user_id: int
    token: Optional[UUID]
    updated_at: Optional[datetime]
    id: Optional[int]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaResponse: ...

class UserTokenSchemaResponseWithPermissionsTokenWrite(AwesomeBaseModel):
    """response schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]
    updated_at: Optional[datetime]
    id: Optional[int]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaResponseWithPermissionsTokenWrite: ...

class UserTokenSchemaResponseWithPermissionsTokenRead(AwesomeBaseModel):
    """response schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]
    updated_at: Optional[datetime]
    id: Optional[int]
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaResponseWithPermissionsTokenRead: ...

class UserTokenSchemaUpdate(AwesomeBaseModel):
    """update schema for UserToken model"""

    user_id: Optional[int]
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaUpdate: ...

class UserTokenSchemaUpdateWithPermissionsTokenWrite(AwesomeBaseModel):
    """update schema for UserToken model with permissions token.write"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaUpdateWithPermissionsTokenWrite: ...

class UserTokenSchemaUpdateWithPermissionsTokenRead(AwesomeBaseModel):
    """update schema for UserToken model with permissions token.read"""

    user_id: int
    token: Optional[UUID]

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> UserTokenSchemaUpdateWithPermissionsTokenRead: ...

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
