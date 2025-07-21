# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Literal, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application import Application
from uaproject_backend_schemas.models.balance import Balance
from uaproject_backend_schemas.models.claim import Claim
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.news import News
from uaproject_backend_schemas.models.punishment import Punishment
from uaproject_backend_schemas.models.purchased_item import PurchasedItem
from uaproject_backend_schemas.models.role import Role
from uaproject_backend_schemas.models.ticket import Ticket
from uaproject_backend_schemas.models.ticket_message import TicketMessage
from uaproject_backend_schemas.models.transaction import Transaction
from uaproject_backend_schemas.models.user_token import UserToken
from uaproject_backend_schemas.models.webhook import Webhook

class User(AwesomeModel):
    """Base user model."""

    application: Optional[Application]
    assigned_tickets: list[Ticket]
    authored_tickets: list[Ticket]
    balance: Optional[Balance]
    biography: Optional[str]
    claims_as_claimant: list[Claim]
    claims_as_defendant: list[Claim]
    created_at: datetime
    discord_id: Optional[int]
    files: list[File]
    id: int
    is_superuser: Optional[bool]
    minecraft_nickname: Optional[str]
    news: list[News]
    permissions: dict[str, bool]
    punishments: list[Punishment]
    purchased_items: list[PurchasedItem]
    received_transactions: list[Transaction]
    roles: list[Role]
    ticket_messages: list[TicketMessage]
    token: Optional[UserToken]
    transactions: list[Transaction]
    updated_at: datetime
    webhooks: list[Webhook]
    schemas: UserSchemas
    filter: type[UserFilter]
    sort: type[UserSort]

class UserSchemas:
    """Schemas for the User model."""

    create: UserSchemaCreate
    redis: UserSchemaRedis
    response: UserSchemaResponse
    update: UserSchemaUpdate
    update_admin: UserSchemaUpdateAdmin

class UserSchemaCreate(AwesomeBaseModel):
    """create schema for User model"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaCreate: ...

class UserSchemaCreateWithPermissionsAdmin(AwesomeBaseModel):
    """create schema for User model with permissions .admin"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaCreateWithPermissionsAdmin: ...

class UserSchemaCreateWithPermissionsWriteNickname(AwesomeBaseModel):
    """create schema for User model with permissions .write.nickname"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaCreateWithPermissionsWriteNickname: ...

class UserSchemaRedis(AwesomeBaseModel):
    """redis schema for User model"""

    authored_tickets: Optional[list[Ticket]]
    ticket_messages: Optional[list[TicketMessage]]
    received_transactions: Optional[list[Transaction]]
    application: Optional[Application]
    roles: Optional[list[Role]]
    claims_as_defendant: Optional[list[Claim]]
    discord_id: Optional[int]
    news: Optional[list[News]]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    balance: Optional[Balance]
    assigned_tickets: Optional[list[Ticket]]
    updated_at: Optional[datetime]
    transactions: Optional[list[Transaction]]
    biography: Optional[str]
    id: Optional[int]
    claims_as_claimant: Optional[list[Claim]]
    files: Optional[list[File]]
    token: Optional[UserToken]
    purchased_items: Optional[list[PurchasedItem]]
    punishments: Optional[list[Punishment]]
    webhooks: Optional[list[Webhook]]
    created_at: datetime
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaRedis: ...

class UserSchemaRedisWithPermissionsAdmin(AwesomeBaseModel):
    """redis schema for User model with permissions .admin"""

    authored_tickets: Optional[list[Ticket]]
    ticket_messages: Optional[list[TicketMessage]]
    received_transactions: Optional[list[Transaction]]
    application: Optional[Application]
    roles: Optional[list[Role]]
    claims_as_defendant: Optional[list[Claim]]
    discord_id: Optional[int]
    news: Optional[list[News]]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    balance: Optional[Balance]
    assigned_tickets: Optional[list[Ticket]]
    updated_at: Optional[datetime]
    transactions: Optional[list[Transaction]]
    biography: Optional[str]
    id: Optional[int]
    claims_as_claimant: Optional[list[Claim]]
    files: Optional[list[File]]
    token: Optional[UserToken]
    purchased_items: Optional[list[PurchasedItem]]
    punishments: Optional[list[Punishment]]
    webhooks: Optional[list[Webhook]]
    created_at: datetime
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaRedisWithPermissionsAdmin: ...

class UserSchemaRedisWithPermissionsWriteNickname(AwesomeBaseModel):
    """redis schema for User model with permissions .write.nickname"""

    authored_tickets: Optional[list[Ticket]]
    ticket_messages: Optional[list[TicketMessage]]
    received_transactions: Optional[list[Transaction]]
    application: Optional[Application]
    roles: Optional[list[Role]]
    claims_as_defendant: Optional[list[Claim]]
    discord_id: Optional[int]
    news: Optional[list[News]]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    balance: Optional[Balance]
    assigned_tickets: Optional[list[Ticket]]
    updated_at: Optional[datetime]
    transactions: Optional[list[Transaction]]
    biography: Optional[str]
    id: Optional[int]
    claims_as_claimant: Optional[list[Claim]]
    files: Optional[list[File]]
    token: Optional[UserToken]
    purchased_items: Optional[list[PurchasedItem]]
    punishments: Optional[list[Punishment]]
    webhooks: Optional[list[Webhook]]
    created_at: datetime
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaRedisWithPermissionsWriteNickname: ...

class UserSchemaResponse(AwesomeBaseModel):
    """response schema for User model"""

    id: Optional[int]
    updated_at: Optional[datetime]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    roles: Optional[list[Role]]
    created_at: datetime
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponse: ...

class UserSchemaResponseWithPermissionsAdmin(AwesomeBaseModel):
    """response schema for User model with permissions .admin"""

    id: Optional[int]
    updated_at: Optional[datetime]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    roles: Optional[list[Role]]
    created_at: datetime
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseWithPermissionsAdmin: ...

class UserSchemaResponseWithPermissionsWriteNickname(AwesomeBaseModel):
    """response schema for User model with permissions .write.nickname"""

    id: Optional[int]
    updated_at: Optional[datetime]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    biography: Optional[str]
    roles: Optional[list[Role]]
    created_at: datetime
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaResponseWithPermissionsWriteNickname: ...

class UserSchemaUpdate(AwesomeBaseModel):
    """update schema for User model"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdate: ...

class UserSchemaUpdateWithPermissionsAdmin(AwesomeBaseModel):
    """update schema for User model with permissions .admin"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateWithPermissionsAdmin: ...

class UserSchemaUpdateWithPermissionsWriteNickname(AwesomeBaseModel):
    """update schema for User model with permissions .write.nickname"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateWithPermissionsWriteNickname: ...

class UserSchemaUpdateAdmin(AwesomeBaseModel):
    """update_admin schema for User model"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateAdmin: ...

class UserSchemaUpdateAdminWithPermissionsAdmin(AwesomeBaseModel):
    """update_admin schema for User model with permissions .admin"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateAdminWithPermissionsAdmin: ...

class UserSchemaUpdateAdminWithPermissionsWriteNickname(AwesomeBaseModel):
    """update_admin schema for User model with permissions .write.nickname"""

    biography: Optional[str]
    discord_id: Optional[int]
    minecraft_nickname: Optional[str]
    is_superuser: Optional[bool]
    permissions: dict[str, bool]

    def with_permissions(
        self, permissions: list[Literal[".admin", ".write.nickname"]]
    ) -> UserSchemaUpdateAdminWithPermissionsWriteNickname: ...

class UserFilter(BaseModel):
    """Pydantic-class for filtering the User model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    discord_id: Optional[int] = None
    min_discord_id: Optional[int] = None
    max_discord_id: Optional[int] = None
    minecraft_nickname: Optional[str] = None
    is_superuser: Optional[bool] = None
    biography: Optional[str] = None
    roles_id: Optional[int] = None
    roles_name: Optional[str] = None
    token_id: Optional[int] = None
    punishments_id: Optional[int] = None
    balance_id: Optional[int] = None
    application_id: Optional[int] = None
    transactions_id: Optional[int] = None
    received_transactions_id: Optional[int] = None
    webhooks_id: Optional[int] = None
    webhooks_name: Optional[str] = None
    claims_as_claimant_id: Optional[int] = None
    claims_as_defendant_id: Optional[int] = None
    news_id: Optional[int] = None
    authored_tickets_id: Optional[int] = None
    assigned_tickets_id: Optional[int] = None
    ticket_messages_id: Optional[int] = None
    files_id: Optional[int] = None
    purchased_items_id: Optional[int] = None

class UserSort(StrEnum):
    """Enum for sorting the User model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
