# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.ticket import TicketPriority, TicketStatus
from uaproject_backend_schemas.models.ticket_message import TicketMessage
from uaproject_backend_schemas.models.user import User

class Ticket(AwesomeModel):
    """Base ticket model."""

    id: int
    updated_at: datetime
    title: str
    description: str
    author_id: int
    assigned_to_id: Optional[int]
    added_user_ids: List[int]
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    author: Optional[User]
    assigned_to: Optional[User]
    messages: Optional[List[TicketMessage]]
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

    title: str
    description: str
    author_id: int
    status: TicketStatus
    priority: TicketPriority
    author: Optional[User]
    assigned_to: Optional[User]
    messages: Optional[List[TicketMessage]]

class TicketSchemaUpdate(AwesomeBaseModel):
    """update schema for Ticket model"""

    title: str
    description: str

class TicketSchemaUpdateAssign(AwesomeBaseModel):
    """update_assign schema for Ticket model"""

    assigned_to_id: Optional[int]
    added_user_ids: List[int]
    status: TicketStatus
    priority: TicketPriority

class TicketSchemaResponse(AwesomeBaseModel):
    """response schema for Ticket model"""

    id: int
    updated_at: datetime
    title: str
    description: str
    author_id: int
    assigned_to_id: Optional[int]
    added_user_ids: List[int]
    status: TicketStatus
    priority: TicketPriority
    author: Optional[User]
    assigned_to: Optional[User]
    messages: Optional[List[TicketMessage]]

class TicketSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for Ticket model"""

    id: int
    updated_at: datetime
    title: str
    description: str
    author_id: int
    assigned_to_id: Optional[int]
    added_user_ids: List[int]
    status: TicketStatus
    priority: TicketPriority
    author: Optional[User]
    assigned_to: Optional[User]
    messages: Optional[List[TicketMessage]]

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

    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
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
    messages_id: Optional[Any] = None

class TicketSort(StrEnum):
    """Enum for sorting the Ticket model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
