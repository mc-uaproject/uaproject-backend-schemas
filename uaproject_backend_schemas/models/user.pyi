# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application import Application
from uaproject_backend_schemas.models.balance import Balance
from uaproject_backend_schemas.models.claim import Claim
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
    access: Optional[bool]
    created_at: datetime
    user_permissions: List
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
    schemas: UserSchemas
    scopes: UserScopes
    filters: UserFilters
    sorts: UserSorts
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

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserSchemaCreate: ...

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

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserSchemaCreateWithPermissionsAdmin: ...

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

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserSchemaUpdate: ...

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

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserSchemaUpdateWithPermissionsAdmin: ...

class UserSchemaUpdateAdmin(AwesomeBaseModel):
    """update_admin schema for User model"""

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
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserSchemaUpdateAdmin: ...

class UserSchemaUpdateAdminWithPermissionsAdmin(AwesomeBaseModel):
    """update_admin schema for User model with permissions .admin"""

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
    claims_as_claimant: Optional[List[Claim]]
    claims_as_defendant: Optional[List[Claim]]
    news: Optional[List[News]]
    authored_tickets: Optional[List[Ticket]]
    assigned_tickets: Optional[List[Ticket]]
    ticket_messages: Optional[List[TicketMessage]]

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserSchemaUpdateAdminWithPermissionsAdmin: ...

class UserSchemaResponse(AwesomeBaseModel):
    """response schema for User model"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserSchemaResponse: ...

class UserSchemaResponseWithPermissionsAdmin(AwesomeBaseModel):
    """response schema for User model with permissions .admin"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserSchemaResponseWithPermissionsAdmin: ...

class UserSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for User model"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserSchemaResponseSelf: ...

class UserSchemaResponseSelfWithPermissionsAdmin(AwesomeBaseModel):
    """response_self schema for User model with permissions .admin"""

    id: int
    updated_at: datetime
    created_at: datetime
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    access: Optional[bool]

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserSchemaResponseSelfWithPermissionsAdmin: ...

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
        self, permissions: list[Literal[".admin"]]
    ) -> UserScopeMinecraftNickname: ...

class UserScopeMinecraftNicknameWithPermissionsAdmin(AwesomeBaseModel):
    """minecraft_nickname schema for User model with permissions .admin"""

    id: int
    minecraft_nickname: Optional[str]

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserScopeMinecraftNicknameWithPermissionsAdmin: ...

class UserScopeDiscordId(AwesomeBaseModel):
    """discord_id schema for User model"""

    id: int
    discord_id: Optional[int]

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserScopeDiscordId: ...

class UserScopeDiscordIdWithPermissionsAdmin(AwesomeBaseModel):
    """discord_id schema for User model with permissions .admin"""

    id: int
    discord_id: Optional[int]

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserScopeDiscordIdWithPermissionsAdmin: ...

class UserScopeSuperuser(AwesomeBaseModel):
    """superuser schema for User model"""

    id: int
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    updated_at: datetime
    created_at: datetime

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserScopeSuperuser: ...

class UserScopeSuperuserWithPermissionsAdmin(AwesomeBaseModel):
    """superuser schema for User model with permissions .admin"""

    id: int
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    updated_at: datetime
    created_at: datetime

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserScopeSuperuserWithPermissionsAdmin: ...

class UserScopeAccess(AwesomeBaseModel):
    """access schema for User model"""

    id: int
    access: Optional[bool]

    def with_permissions(self, permissions: list[Literal[".admin"]]) -> UserScopeAccess: ...

class UserScopeAccessWithPermissionsAdmin(AwesomeBaseModel):
    """access schema for User model with permissions .admin"""

    id: int
    access: Optional[bool]

    def with_permissions(
        self, permissions: list[Literal[".admin"]]
    ) -> UserScopeAccessWithPermissionsAdmin: ...

class UserFilters:
    """Declarative filters for the User model."""

class UserFilter(BaseModel):
    """Pydantic-class for filtering the User model."""

class UserSorts:
    """Declarative sorts for the User model."""

class UserSort(StrEnum):
    """Enum for sorting the User model."""
