# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.ticket import TicketPriority, TicketStatus
from uaproject_backend_schemas.models.ticket_message import TicketMessage
from uaproject_backend_schemas.models.user import User

class Ticket(AwesomeModel):
    """Base ticket model."""

    added_user_ids: list[int]
    assigned_to: Optional[User]
    assigned_to_id: Optional[int]
    author: Optional[User]
    author_id: int
    created_at: datetime
    description: str
    id: int
    messages: list[TicketMessage]
    priority: TicketPriority
    status: TicketStatus
    title: str
    updated_at: datetime
    schemas: TicketSchemas
    filter: type[TicketFilter]
    sort: type[TicketSort]

class TicketSchemas:
    """Schemas for the Ticket model."""

    create: TicketSchemaCreate
    redis: TicketSchemaRedis
    response: TicketSchemaResponse
    response_self: TicketSchemaResponseSelf
    update: TicketSchemaUpdate
    update_assign: TicketSchemaUpdateAssign

class TicketSchemaCreate(AwesomeBaseModel):
    """create schema for Ticket model"""

    author_id: Optional[int]
    priority: Optional[TicketPriority]
    title: Optional[str]
    status: Optional[TicketStatus]
    description: Optional[str]
    created_at: datetime

class TicketSchemaRedis(AwesomeBaseModel):
    """redis schema for Ticket model"""

    id: Optional[int]
    author_id: Optional[int]
    updated_at: Optional[datetime]
    priority: Optional[TicketPriority]
    added_user_ids: Optional[list[int]]
    author: Optional[User]
    title: Optional[str]
    assigned_to_id: Optional[int]
    assigned_to: Optional[User]
    status: Optional[TicketStatus]
    messages: Optional[list[TicketMessage]]
    description: Optional[str]
    created_at: datetime

class TicketSchemaResponse(AwesomeBaseModel):
    """response schema for Ticket model"""

    id: Optional[int]
    author_id: int
    updated_at: Optional[datetime]
    priority: TicketPriority
    added_user_ids: list[int]
    title: str
    assigned_to_id: Optional[int]
    status: TicketStatus
    description: str
    created_at: datetime

class TicketSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for Ticket model"""

    id: Optional[int]
    author_id: int
    updated_at: Optional[datetime]
    priority: TicketPriority
    added_user_ids: list[int]
    title: str
    assigned_to_id: Optional[int]
    status: TicketStatus
    description: str
    created_at: datetime

class TicketSchemaUpdate(AwesomeBaseModel):
    """update schema for Ticket model"""

    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    created_at: datetime

class TicketSchemaUpdateAssign(AwesomeBaseModel):
    """update_assign schema for Ticket model"""

    id: Optional[int]
    assigned_to_id: Optional[int]
    added_user_ids: Optional[list[int]]
    status: Optional[TicketStatus]
    priority: Optional[TicketPriority]
    created_at: datetime

class TicketFilter(BaseModel):
    """Pydantic-class for filtering the Ticket model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    author_id: Optional[int] = None
    min_author_id: Optional[int] = None
    max_author_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    min_assigned_to_id: Optional[int] = None
    max_assigned_to_id: Optional[int] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    messages_id: Optional[int] = None

class TicketSort(StrEnum):
    """Enum for sorting the Ticket model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
