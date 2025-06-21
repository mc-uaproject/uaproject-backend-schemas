# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application import Application
from uaproject_backend_schemas.models.balance import Balance
from uaproject_backend_schemas.models.claim import Claim
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.news import News
from uaproject_backend_schemas.models.punishment import Punishment
from uaproject_backend_schemas.models.role import Role
from uaproject_backend_schemas.models.ticket import Ticket
from uaproject_backend_schemas.models.ticket_message import TicketMessage
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
    created_at: datetime
    permissions: Dict[str, bool]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]
    schemas: UserSchemas
    scopes: UserScopes
    filter: type[UserFilter]
    sort: type[UserSort]

class UserSchemas:
    """Schemas for the User model."""

    create: UserSchemaCreate
    update: UserSchemaUpdate
    update_admin: UserSchemaUpdateAdmin
    response: UserSchemaResponse
    response_self: UserSchemaResponseSelf

class UserSchemaCreate(AwesomeBaseModel):
    """create schema for User model"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaCreate: ...

class UserSchemaCreateWithPermissionsAdmin(AwesomeBaseModel):
    """create schema for User model with permissions .admin"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaCreateWithPermissionsAdmin: ...

class UserSchemaCreateWithPermissionsWriteNickname(AwesomeBaseModel):
    """create schema for User model with permissions .write.nickname"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaCreateWithPermissionsWriteNickname: ...

class UserSchemaUpdate(AwesomeBaseModel):
    """update schema for User model"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdate: ...

class UserSchemaUpdateWithPermissionsAdmin(AwesomeBaseModel):
    """update schema for User model with permissions .admin"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateWithPermissionsAdmin: ...

class UserSchemaUpdateWithPermissionsWriteNickname(AwesomeBaseModel):
    """update schema for User model with permissions .write.nickname"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateWithPermissionsWriteNickname: ...

class UserSchemaUpdateAdmin(AwesomeBaseModel):
    """update_admin schema for User model"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateAdmin: ...

class UserSchemaUpdateAdminWithPermissionsAdmin(AwesomeBaseModel):
    """update_admin schema for User model with permissions .admin"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateAdminWithPermissionsAdmin: ...

class UserSchemaUpdateAdminWithPermissionsWriteNickname(AwesomeBaseModel):
    """update_admin schema for User model with permissions .write.nickname"""

    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    roles: Optional[List[Role]]
    token: Optional[Token]
    punishments: Optional[List[Punishment]]
    balance: Optional[Balance]
    application: Optional[Application]
    transactions: Optional[List[Transaction]]
    received_transactions: Optional[List[Transaction]]
    webhooks: Optional[List[Webhook]]
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]
    files: Optional[List[File]]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateAdminWithPermissionsWriteNickname: ...

class UserSchemaResponse(AwesomeBaseModel):
    """response schema for User model"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponse: ...

class UserSchemaResponseWithPermissionsAdmin(AwesomeBaseModel):
    """response schema for User model with permissions .admin"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseWithPermissionsAdmin: ...

class UserSchemaResponseWithPermissionsWriteNickname(AwesomeBaseModel):
    """response schema for User model with permissions .write.nickname"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseWithPermissionsWriteNickname: ...

class UserSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for User model"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseSelf: ...

class UserSchemaResponseSelfWithPermissionsAdmin(AwesomeBaseModel):
    """response_self schema for User model with permissions .admin"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseSelfWithPermissionsAdmin: ...

class UserSchemaResponseSelfWithPermissionsWriteNickname(AwesomeBaseModel):
    """response_self schema for User model with permissions .write.nickname"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseSelfWithPermissionsWriteNickname: ...

class UserScopes:
    """Scopes for the User model."""

    minecraft_nickname: UserScopeMinecraftNickname
    discord_id: UserScopeDiscordId
    superuser: UserScopeSuperuser
    access: UserScopeAccess

class UserScopeMinecraftNickname(AwesomeBaseModel):
    """minecraft_nickname schema for User model"""

    id: int
    minecraft_nickname: Optional[str]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeMinecraftNickname: ...

class UserScopeMinecraftNicknameWithPermissionsAdmin(AwesomeBaseModel):
    """minecraft_nickname schema for User model with permissions .admin"""

    id: int
    minecraft_nickname: Optional[str]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeMinecraftNicknameWithPermissionsAdmin: ...

class UserScopeMinecraftNicknameWithPermissionsWriteNickname(AwesomeBaseModel):
    """minecraft_nickname schema for User model with permissions .write.nickname"""

    id: int
    minecraft_nickname: Optional[str]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeMinecraftNicknameWithPermissionsWriteNickname: ...

class UserScopeDiscordId(AwesomeBaseModel):
    """discord_id schema for User model"""

    id: int
    discord_id: Optional[int]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeDiscordId: ...

class UserScopeDiscordIdWithPermissionsAdmin(AwesomeBaseModel):
    """discord_id schema for User model with permissions .admin"""

    id: int
    discord_id: Optional[int]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeDiscordIdWithPermissionsAdmin: ...

class UserScopeDiscordIdWithPermissionsWriteNickname(AwesomeBaseModel):
    """discord_id schema for User model with permissions .write.nickname"""

    id: int
    discord_id: Optional[int]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeDiscordIdWithPermissionsWriteNickname: ...

class UserScopeSuperuser(AwesomeBaseModel):
    """superuser schema for User model"""

    id: int
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    updated_at: datetime
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeSuperuser: ...

class UserScopeSuperuserWithPermissionsAdmin(AwesomeBaseModel):
    """superuser schema for User model with permissions .admin"""

    id: int
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    updated_at: datetime
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeSuperuserWithPermissionsAdmin: ...

class UserScopeSuperuserWithPermissionsWriteNickname(AwesomeBaseModel):
    """superuser schema for User model with permissions .write.nickname"""

    id: int
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    updated_at: datetime
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeSuperuserWithPermissionsWriteNickname: ...

class UserScopeAccess(AwesomeBaseModel):
    """access schema for User model"""

    id: int
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeAccess: ...

class UserScopeAccessWithPermissionsAdmin(AwesomeBaseModel):
    """access schema for User model with permissions .admin"""

    id: int
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeAccessWithPermissionsAdmin: ...

class UserScopeAccessWithPermissionsWriteNickname(AwesomeBaseModel):
    """access schema for User model with permissions .write.nickname"""

    id: int
    access: Any

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserScopeAccessWithPermissionsWriteNickname: ...

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
    roles_id: Optional[Any] = None
    roles_name: Optional[Any] = None
    token_id: Optional[Any] = None
    punishments_id: Optional[Any] = None
    balance_id: Optional[Any] = None
    application_id: Optional[Any] = None
    transactions_id: Optional[Any] = None
    received_transactions_id: Optional[Any] = None
    webhooks_id: Optional[Any] = None
    claims_as_claimant_id: Optional[Any] = None
    claims_as_defendant_id: Optional[Any] = None
    news_id: Optional[Any] = None
    authored_tickets_id: Optional[Any] = None
    assigned_tickets_id: Optional[Any] = None
    ticket_messages_id: Optional[Any] = None
    files_id: Optional[Any] = None

class UserSort(StrEnum):
    """Enum for sorting the User model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
