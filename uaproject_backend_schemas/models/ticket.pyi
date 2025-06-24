# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

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
    description: str
    id: int
    messages: list[TicketMessage]
    priority: TicketPriority
    status: TicketStatus
    title: str
    updated_at: datetime
    schemas: TicketSchemas
    scopes: TicketScopes
    filter: type[TicketFilter]
    sort: type[TicketSort]

class TicketSchemas:
    """Schemas for the Ticket model."""

    create: TicketSchemaCreate
    update: TicketSchemaUpdate
    update_assign: TicketSchemaUpdateAssign
    response: TicketSchemaResponse
    response_self: TicketSchemaResponseSelf

class TicketSchemaCreate(AwesomeBaseModel):
    """create schema for Ticket model"""

    title: Optional[str]
    description: Optional[str]
    author_id: Optional[int]
    status: Optional[TicketStatus]
    priority: Optional[TicketPriority]
    author: Optional[User]
    assigned_to: Optional[User]
    messages: Optional[list[TicketMessage]]

class TicketSchemaUpdate(AwesomeBaseModel):
    """update schema for Ticket model"""

    title: Optional[str]
    description: Optional[str]

class TicketSchemaUpdateAssign(AwesomeBaseModel):
    """update_assign schema for Ticket model"""

    assigned_to_id: Optional[int]
    added_user_ids: Optional[list[int]]
    status: Optional[TicketStatus]
    priority: Optional[TicketPriority]

class TicketSchemaResponse(AwesomeBaseModel):
    """response schema for Ticket model"""

    updated_at: datetime
    id: int
    title: str
    description: str
    author_id: int
    assigned_to_id: Optional[int]
    added_user_ids: list[int]
    status: TicketStatus
    priority: TicketPriority
    author: Optional[User]
    assigned_to: Optional[User]
    messages: list[TicketMessage]

class TicketSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for Ticket model"""

    updated_at: datetime
    id: int
    title: str
    description: str
    author_id: int
    assigned_to_id: Optional[int]
    added_user_ids: list[int]
    status: TicketStatus
    priority: TicketPriority
    author: Optional[User]
    assigned_to: Optional[User]
    messages: list[TicketMessage]

class TicketScopes:
    """Scopes for the Ticket model."""

    status: TicketScopeStatus
    priority: TicketScopePriority
    assignment: TicketScopeAssignment

class TicketScopeStatus(AwesomeBaseModel):
    """status schema for Ticket model"""

    id: int
    author_id: int
    assigned_to_id: Optional[int]
    status: TicketStatus

class TicketScopePriority(AwesomeBaseModel):
    """priority schema for Ticket model"""

    id: int
    priority: TicketPriority

class TicketScopeAssignment(AwesomeBaseModel):
    """assignment schema for Ticket model"""

    id: int
    author_id: int
    assigned_to_id: Optional[int]

class TicketFilter(BaseModel):
    """Pydantic-class for filtering the Ticket model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    title: Optional[str] = None
    description: Optional[str] = None
    author_id: Optional[int] = None
    min_author_id: Optional[Any] = None
    max_author_id: Optional[Any] = None
    assigned_to_id: Optional[int] = None
    min_assigned_to_id: Optional[Any] = None
    max_assigned_to_id: Optional[Any] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None

class TicketSort(StrEnum):
    """Enum for sorting the Ticket model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
