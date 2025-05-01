# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
from typing import Literal, Optional, Type, overload

from uaproject_backend_schemas.awesome.model import AwesomeModel, classproperty
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel, AwesomeField

class User(AwesomeModel):
    """Base user model."""

    @classproperty
    def schemas(cls) -> UserSchemas | Type[UserSchemas] | Type[AwesomeModel.Schemas]: ...
    @classproperty
    def scopes(cls) -> UserScopes | Type[UserScopes] | Type[AwesomeModel.Scopes]: ...

class UserSchemas(AwesomeModel.Schemas):
    """Schemas for the user model."""

    create: Type[UserSchemaCreate] = ...

    @overload
    def __getattr__(self, item: Literal["create"]) -> Type[UserSchemaCreate]: ...
    def __getattr__(self, item: str) -> Type[AwesomeBaseModel]: ...

class UserScopes(AwesomeModel.Scopes):
    """Visibility scopes for the user model."""

    public: UserScopePublic
    private: UserScopePrivate
    create: UserScopeCreate

class UserSchemaCreate(AwesomeBaseModel):
    """create schema for User model"""

    id: Optional[int]
    name: str = AwesomeField(exclude_permissions=["private"])
    age: int = AwesomeField(include_permissions=["private"])

class UserSchemaCreateWithPermissions(AwesomeBaseModel):
    """create schema for User model with permissions"""

    id: Optional[int]
    name: str = AwesomeField(exclude_permissions=["private"])
    age: int = AwesomeField(include_permissions=["private"])

    def with_permissions(
        self, permissions: list[Literal["private"]]
    ) -> UserSchemaCreateWithPermissionsPrivate | UserSchemaCreateWithPermissions: ...

class UserSchemaCreateWithPermissionsPrivate(AwesomeBaseModel):
    """create schema for User model with permissions private"""

    id: Optional[int]
    age: int = AwesomeField(include_permissions=["private"])

    def with_permissions(
        self, permissions: list[Literal["private"]]
    ) -> UserSchemaCreateWithPermissionsPrivate | UserSchemaCreateWithPermissions: ...

class UserScopePublic(AwesomeBaseModel):
    """public visibility scope for User model"""

    id: Optional[int]
    name: str

class UserScopePublicWithPermissions(AwesomeBaseModel):
    """public visibility scope for User model with permissions"""

    id: Optional[int]
    name: str

class UserScopePublicWithPermissionsPrivate(AwesomeBaseModel):
    """public visibility scope for User model with permissions private"""

    id: Optional[int]

    def with_permissions(
        self, permissions: list[Literal["private"]]
    ) -> UserScopePublicWithPermissionsPrivate | UserScopePublicWithPermissions: ...

class UserScopePrivate(AwesomeBaseModel):
    """private visibility scope for User model"""

    id: Optional[int]
    name: str

class UserScopePrivateWithPermissions(AwesomeBaseModel):
    """private visibility scope for User model with permissions"""

    id: Optional[int]
    name: str

class UserScopePrivateWithPermissionsPrivate(AwesomeBaseModel):
    """private visibility scope for User model with permissions private"""

    id: Optional[int]

    def with_permissions(
        self, permissions: list[Literal["private"]]
    ) -> UserScopePrivateWithPermissionsPrivate | UserScopePrivateWithPermissions: ...

class UserScopeCreate(AwesomeBaseModel):
    """create visibility scope for User model"""

    id: Optional[int]
    name: str
    age: int

class UserScopeCreateWithPermissions(AwesomeBaseModel):
    """create visibility scope for User model with permissions"""

    id: Optional[int]
    name: str
    age: int

class UserScopeCreateWithPermissionsPrivate(AwesomeBaseModel):
    """create visibility scope for User model with permissions private"""

    id: Optional[int]
    age: int

    def with_permissions(
        self, permissions: list[Literal["private"]]
    ) -> UserScopeCreateWithPermissionsPrivate | UserScopeCreateWithPermissions: ...
