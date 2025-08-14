# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

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
    created_at: datetime
    edited_at: Optional[str]
    id: int
    is_system_message: bool
    ticket: Optional[Ticket]
    ticket_id: int
    updated_at: datetime
    schemas: TicketMessageSchemas
    filter: type[TicketMessageFilter]
    sort: type[TicketMessageSort]

class TicketMessageSchemas:
    """Schemas for the TicketMessage model."""

    create: TicketMessageSchemaCreate
    redis: TicketMessageSchemaRedis
    response: TicketMessageSchemaResponse
    response_with_author: TicketMessageSchemaResponseWithAuthor
    update: TicketMessageSchemaUpdate

class TicketMessageSchemaCreate(AwesomeBaseModel):
    """create schema for TicketMessage model"""

    content: Optional[str]
    ticket_id: Optional[int]
    attachment_file_ids: Optional[list[int]]

class TicketMessageSchemaRedis(AwesomeBaseModel):
    """redis schema for TicketMessage model"""

    edited_at: Optional[str]
    author_id: Optional[int]
    is_system_message: Optional[bool]
    attachment_files: Optional[list[File]]
    id: Optional[int]
    ticket: Optional[Ticket]
    updated_at: Optional[datetime]
    content: Optional[str]
    ticket_id: Optional[int]
    attachment_file_ids: Optional[list[int]]
    author: Optional[User]
    created_at: datetime

class TicketMessageSchemaResponse(AwesomeBaseModel):
    """response schema for TicketMessage model"""

    edited_at: Optional[str]
    author_id: int
    is_system_message: Optional[bool]
    id: Optional[int]
    updated_at: Optional[datetime]
    content: str
    ticket_id: int
    attachment_file_ids: Optional[list[int]]
    created_at: datetime

class TicketMessageSchemaResponseWithAuthor(AwesomeBaseModel):
    """response_with_author schema for TicketMessage model"""

    id: Optional[int]
    ticket_id: int
    author_id: int
    content: str
    attachment_file_ids: Optional[list[int]]
    is_system_message: Optional[bool]
    edited_at: Optional[str]
    updated_at: Optional[datetime]
    created_at: datetime

class TicketMessageSchemaUpdate(AwesomeBaseModel):
    """update schema for TicketMessage model"""

    id: Optional[int]
    content: Optional[str]
    created_at: datetime

class TicketMessageFilter(BaseModel):
    """Pydantic-class for filtering the TicketMessage model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    ticket_id: Optional[int] = None
    min_ticket_id: Optional[int] = None
    max_ticket_id: Optional[int] = None
    author_id: Optional[int] = None
    min_author_id: Optional[int] = None
    max_author_id: Optional[int] = None
    content: Optional[str] = None
    is_system_message: Optional[bool] = None
    edited_at: Optional[str] = None
    attachment_files_id: Optional[int] = None

class TicketMessageSort(StrEnum):
    """Enum for sorting the TicketMessage model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
