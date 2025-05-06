# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.filters import FilterDefinition
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.sorts import SortDefinition

class User(AwesomeModel):
    """Base user model."""

    schemas: UserSchemas
    scopes: UserScopes
    filters: UserFilters
    sorts: UserSorts
    filter: type[UserFilter]
    sort: type[UserSort]

class UserSchemas:
    """Schemas for the user model."""

    create: UserSchemaCreate
    update: UserSchemaUpdate
    response: UserSchemaResponse

class UserScopes:
    """Visibility scopes for the user model."""

    minecraft_nickname: UserScopeMinecraftNickname
    discord_id: UserScopeDiscordId
    superuser: UserScopeSuperuser
    access: UserScopeAccess

class UserFilters:
    """Declarative filters for the User model."""

    ByAccess: type
    ByBiography: type
    ByDiscordId: type
    ById: type
    ByIsSuperuser: type
    ByMinecraftNickname: type
    ByRoleName: type

class UserFilterByAccess(FilterDefinition):
    """Фільтрація за доступом"""

    field: str = "access"

class UserFilterByBiography(FilterDefinition):
    """Фільтрація за біографією (пошук по підрядку)"""

    field: str = "biography"

class UserFilterByDiscordId(FilterDefinition):
    """Фільтрація за Discord ID"""

    field: str = "discord_id"

class UserFilterById(FilterDefinition):
    """Фільтрація за ID користувача"""

    field: str = "id"

class UserFilterByIsSuperuser(FilterDefinition):
    """Фільтрація за статусом суперкористувача"""

    field: str = "is_superuser"

class UserFilterByMinecraftNickname(FilterDefinition):
    """Фільтрація за ніком Minecraft"""

    field: str = "minecraft_nickname"

class UserFilterByRoleName(FilterDefinition):
    """Фільтрація за назвою ролі"""

    field: str = "role_name"

class UserSorts:
    """Declarative sorts for the User model."""

    ByCreatedAt: type
    ByDiscordId: type
    ById: type
    ByMinecraftNickname: type
    ByRoleWeight: type
    ByUpdatedAt: type

class UserSortByCreatedAt(SortDefinition):
    """Сортування за датою створення"""

    field: str = "created_at"
    direction: str = "asc"

class UserSortByDiscordId(SortDefinition):
    """Сортування за Discord ID"""

    field: str = "discord_id"
    direction: str = "asc"

class UserSortById(SortDefinition):
    """Сортування за ID"""

    field: str = "id"
    direction: str = "asc"

class UserSortByMinecraftNickname(SortDefinition):
    """Сортування за ніком Minecraft"""

    field: str = "minecraft_nickname"
    direction: str = "asc"

class UserSortByRoleWeight(SortDefinition):
    """Сортування за вагою ролі"""

    field: str = "role_weight"
    direction: str = "asc"

class UserSortByUpdatedAt(SortDefinition):
    """Сортування за датою оновлення"""

    field: str = "updated_at"
    direction: str = "asc"

class UserFilter(BaseModel):
    """Pydantic-class for filtering the User model."""

    access: Optional[bool] = None
    biography: Optional[str] = None
    discord_id: Optional[int] = None
    id: Optional[int] = None
    is_superuser: Optional[bool] = None
    minecraft_nickname: Optional[str] = None
    role_name: Optional[Any] = None

class UserSort(StrEnum):
    """Enum for sorting the User model."""

    BYCREATEDAT = "created_at"
    BYDISCORDID = "discord_id"
    BYID = "id"
    BYMINECRAFTNICKNAME = "minecraft_nickname"
    BYROLEWEIGHT = "role_weight"
    BYUPDATEDAT = "updated_at"

class UserSchemaCreate(AwesomeBaseModel):
    """Create schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

class UserSchemaUpdate(AwesomeBaseModel):
    """Update schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

class UserSchemaResponse(AwesomeBaseModel):
    """Response schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

class UserScopeMinecraftNickname(AwesomeBaseModel):
    """minecraft_nickname visibility scope for User model"""

    id: int
    minecraft_nickname: Optional[str]

class UserScopeDiscordId(AwesomeBaseModel):
    """discord_id visibility scope for User model"""

    id: int
    discord_id: Optional[int]

class UserScopeSuperuser(AwesomeBaseModel):
    """superuser visibility scope for User model"""

    id: int
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    updated_at: datetime

class UserScopeAccess(AwesomeBaseModel):
    """access visibility scope for User model"""

    id: int
    access: Optional[bool]
