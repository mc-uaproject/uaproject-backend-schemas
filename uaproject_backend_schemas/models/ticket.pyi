# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.ticket import TicketPriority, TicketStatus
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
    author: Optional[User]
    assigned_to: Optional[User]
    schemas: TicketSchemas
    scopes: TicketScopes
    filters: TicketFilters
    sorts: TicketSorts
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

class TicketFilters:
    """Declarative filters for the Ticket model."""

class TicketFilter(BaseModel):
    """Pydantic-class for filtering the Ticket model."""

class TicketSorts:
    """Declarative sorts for the Ticket model."""

class TicketSort(StrEnum):
    """Enum for sorting the Ticket model."""
