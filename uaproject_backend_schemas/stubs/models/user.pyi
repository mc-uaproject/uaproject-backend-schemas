# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Optional

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel
from uaproject_backend_schemas.models.user import User

class User(AwesomeModel):
    """Base user model."""

    schemas: UserSchemas
    scopes: UserScopes

class UserSchemas:
    """Schemas for the user model."""

class UserScopes:
    """Visibility scopes for the user model."""

    minecraft_nickname: UserScopeMinecraftNickname
    discord_id: UserScopeDiscordId
    superuser: UserScopeSuperuser
    access: UserScopeAccess

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
