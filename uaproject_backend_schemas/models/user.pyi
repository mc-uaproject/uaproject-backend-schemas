# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application import Application
from uaproject_backend_schemas.models.balance import Balance
from uaproject_backend_schemas.models.punishment import Punishment
from uaproject_backend_schemas.models.role import Role
from uaproject_backend_schemas.models.transaction import Transaction
from uaproject_backend_schemas.models.user_token import Token
from uaproject_backend_schemas.models.webhook import Webhook

class User(AwesomeModel):
    """Base user model."""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    schemas: UserSchemas
    scopes: UserScopes
    filters: UserFilters
    filter: type[UserFilter]

class UserSchemas:
    """Schemas for the User model."""

class UserScopes:
    """Scopes for the User model."""

    minecraft_nickname: UserScopeMinecraftNickname

class UserScopeMinecraftNickname(AwesomeBaseModel):
    """minecraft_nickname schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    discord_id: UserScopeDiscordId

class UserScopeDiscordId(AwesomeBaseModel):
    """discord_id schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    superuser: UserScopeSuperuser

class UserScopeSuperuser(AwesomeBaseModel):
    """superuser schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    access: UserScopeAccess

class UserScopeAccess(AwesomeBaseModel):
    """access schema for User model"""

    id: int
    updated_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

class UserFilters:
    """Declarative filters for the User model."""

class UserFilter(BaseModel):
    """Pydantic-class for filtering the User model."""

    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    discord_id: Optional[int] = None
    min_discord_id: Optional[Any] = None
    max_discord_id: Optional[Any] = None
    minecraft_nickname: Optional[str] = None
    is_superuser: Optional[bool] = None
    biography: Optional[str] = None
    access: Optional[bool] = None
