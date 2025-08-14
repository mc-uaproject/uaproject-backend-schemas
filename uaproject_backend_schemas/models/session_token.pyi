# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.session_token import TokenType
from uaproject_backend_schemas.models.user import User

class SessionToken(AwesomeModel):
    """Base sessiontoken model."""

    created_at: datetime
    device_id: Optional[str]
    expires_at: datetime
    id: int
    ip_address: Optional[str]
    is_bot: bool
    last_used_at: Optional[datetime]
    login_method: str
    revoked: bool
    session_id: str
    token_type: TokenType
    updated_at: datetime
    user: User
    user_agent: Optional[str]
    user_id: int
    schemas: SessionTokenSchemas
    filter: type[SessionTokenFilter]
    sort: type[SessionTokenSort]

class SessionTokenSchemas:
    """Schemas for the SessionToken model."""

    admin_response: SessionTokenSchemaAdminResponse
    create: SessionTokenSchemaCreate
    create_bot: SessionTokenSchemaCreateBot
    redis: SessionTokenSchemaRedis
    response: SessionTokenSchemaResponse
    update: SessionTokenSchemaUpdate

class SessionTokenSchemaAdminResponse(AwesomeBaseModel):
    """admin_response schema for SessionToken model"""

    id: Optional[int]
    session_id: Optional[str]
    user_id: int
    expires_at: datetime
    last_used_at: Optional[datetime]
    revoked: Optional[bool]
    ip_address: Optional[str]
    user_agent: Optional[str]
    device_id: Optional[str]
    login_method: Optional[str]
    created_at: datetime

class SessionTokenSchemaCreate(AwesomeBaseModel):
    """create schema for SessionToken model"""

    token_type: Optional[TokenType]
    is_bot: Optional[bool]
    session_id: Optional[str]
    user_id: Optional[int]
    expires_at: Optional[datetime]
    device_id: Optional[str]
    login_method: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]

class SessionTokenSchemaCreateBot(AwesomeBaseModel):
    """create_bot schema for SessionToken model"""

    token_type: Optional[TokenType]
    is_bot: Optional[bool]
    session_id: Optional[str]
    user_id: Optional[int]
    device_id: Optional[str]
    login_method: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]

class SessionTokenSchemaRedis(AwesomeBaseModel):
    """redis schema for SessionToken model"""

    revoked: Optional[bool]
    token_type: Optional[TokenType]
    is_bot: Optional[bool]
    session_id: Optional[str]
    user: Optional[User]
    user_id: Optional[int]
    last_used_at: Optional[datetime]
    id: Optional[int]
    updated_at: Optional[datetime]
    expires_at: Optional[datetime]
    device_id: Optional[str]
    login_method: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

class SessionTokenSchemaResponse(AwesomeBaseModel):
    """response schema for SessionToken model"""

    id: Optional[int]
    session_id: Optional[str]
    user_id: int
    expires_at: datetime
    last_used_at: Optional[datetime]
    revoked: Optional[bool]
    ip_address: Optional[str]
    user_agent: Optional[str]
    device_id: Optional[str]
    login_method: Optional[str]
    created_at: datetime

class SessionTokenSchemaUpdate(AwesomeBaseModel):
    """update schema for SessionToken model"""

    revoked: Optional[bool]
    token_type: Optional[TokenType]
    is_bot: Optional[bool]
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    device_id: Optional[str]
    login_method: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]

class SessionTokenFilter(BaseModel):
    """Pydantic-class for filtering the SessionToken model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    session_id: Optional[str] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    expires_at: Optional[datetime] = None
    min_expires_at: Optional[datetime] = None
    max_expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    min_last_used_at: Optional[datetime] = None
    max_last_used_at: Optional[datetime] = None
    revoked: Optional[bool] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_id: Optional[str] = None
    login_method: Optional[str] = None
    is_bot: Optional[bool] = None
    token_type: Optional[TokenType] = None

class SessionTokenSort(StrEnum):
    """Enum for sorting the SessionToken model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
