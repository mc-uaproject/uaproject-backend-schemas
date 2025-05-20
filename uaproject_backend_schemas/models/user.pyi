# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import List, Optional

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
