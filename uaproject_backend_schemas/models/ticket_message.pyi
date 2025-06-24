# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.ticket import Ticket
from uaproject_backend_schemas.models.user import User

class TicketMessage(AwesomeModel):
    """Base ticketmessage model."""

    attachment_file_ids: Optional[list[int]]
    attachment_files: list[File]
    author: Optional[User]
    author_id: int
    content: str
    edited_at: Optional[str]
    id: int
    is_system_message: bool
    ticket: Optional[Ticket]
    ticket_id: int
    updated_at: datetime
    schemas: TicketMessageSchemas
    scopes: TicketMessageScopes
    filter: type[TicketMessageFilter]
    sort: type[TicketMessageSort]

class TicketMessageSchemas:
    """Schemas for the TicketMessage model."""

    create: TicketMessageSchemaCreate
    update: TicketMessageSchemaUpdate
    response: TicketMessageSchemaResponse
    response_with_author: TicketMessageSchemaResponseWithAuthor

class TicketMessageSchemaCreate(AwesomeBaseModel):
    """create schema for TicketMessage model"""

    ticket_id: Optional[int]
    content: Optional[str]
    attachment_file_ids: Optional[list[int]]
    ticket: Optional[Ticket]
    author: Optional[User]
    attachment_files: Optional[list[File]]

class TicketMessageSchemaUpdate(AwesomeBaseModel):
    """update schema for TicketMessage model"""

    content: Optional[str]

class TicketMessageSchemaResponse(AwesomeBaseModel):
    """response schema for TicketMessage model"""

    updated_at: datetime
    id: int
    ticket_id: int
    author_id: int
    content: str
    attachment_file_ids: Optional[list[int]]
    is_system_message: bool
    edited_at: Optional[str]
    ticket: Optional[Ticket]
    author: Optional[User]
    attachment_files: list[File]

class TicketMessageSchemaResponseWithAuthor(AwesomeBaseModel):
    """response_with_author schema for TicketMessage model"""

    id: int
    ticket_id: int
    author_id: int
    content: str
    attachment_file_ids: Optional[list[int]]
    is_system_message: bool
    edited_at: Optional[str]
    created_at: datetime
    updated_at: datetime

class TicketMessageScopes:
    """Scopes for the TicketMessage model."""

    ticket_messages: TicketMessageScopeTicketMessages

class TicketMessageScopeTicketMessages(AwesomeBaseModel):
    """ticket_messages schema for TicketMessage model"""

    id: int
    ticket_id: int
    author_id: int
    content: str
    created_at: datetime

class TicketMessageFilter(BaseModel):
    """Pydantic-class for filtering the TicketMessage model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    ticket_id: Optional[int] = None
    min_ticket_id: Optional[Any] = None
    max_ticket_id: Optional[Any] = None
    author_id: Optional[int] = None
    min_author_id: Optional[Any] = None
    max_author_id: Optional[Any] = None
    content: Optional[str] = None
    is_system_message: Optional[bool] = None
    edited_at: Optional[str] = None

class TicketMessageSort(StrEnum):
    """Enum for sorting the TicketMessage model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
