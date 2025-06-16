# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.ticket import Ticket
from uaproject_backend_schemas.models.user import User

class TicketMessage(AwesomeModel):
    """Base ticketmessage model."""

    id: int
    updated_at: datetime
    ticket_id: int
    author_id: int
    content: str
    attachments: Optional[List]
    is_system_message: bool
    edited_at: Optional[str]
    ticket: Optional[Ticket]
    author: Optional[User]
    schemas: TicketMessageSchemas
    scopes: TicketMessageScopes
    filters: TicketMessageFilters
    sorts: TicketMessageSorts
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

    ticket_id: int
    content: str
    attachments: Optional[List]
    ticket: Optional[Ticket]
    author: Optional[User]

class TicketMessageSchemaUpdate(AwesomeBaseModel):
    """update schema for TicketMessage model"""

    content: str

class TicketMessageSchemaResponse(AwesomeBaseModel):
    """response schema for TicketMessage model"""

    id: int
    updated_at: datetime
    ticket_id: int
    author_id: int
    content: str
    attachments: Optional[List]
    is_system_message: bool
    edited_at: Optional[str]
    ticket: Optional[Ticket]
    author: Optional[User]

class TicketMessageSchemaResponseWithAuthor(AwesomeBaseModel):
    """response_with_author schema for TicketMessage model"""

    id: int
    ticket_id: int
    author_id: int
    content: str
    attachments: Optional[List]
    is_system_message: bool
    edited_at: Optional[str]
    created_at: Any
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
    created_at: Any

class TicketMessageFilters:
    """Declarative filters for the TicketMessage model."""

class TicketMessageFilter(BaseModel):
    """Pydantic-class for filtering the TicketMessage model."""

class TicketMessageSorts:
    """Declarative sorts for the TicketMessage model."""

class TicketMessageSort(StrEnum):
    """Enum for sorting the TicketMessage model."""
