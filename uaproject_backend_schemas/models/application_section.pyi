# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType

class ApplicationSection(AwesomeModel):
    """Base applicationsection model."""

    id: int
    updated_at: datetime
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool
    created_at: datetime
    schemas: ApplicationSectionSchemas
    scopes: ApplicationSectionScopes
    filters: ApplicationSectionFilters
    sorts: ApplicationSectionSorts
    filter: type[ApplicationSectionFilter]
    sort: type[ApplicationSectionSort]

class ApplicationSectionSchemas:
    """Schemas for the ApplicationSection model."""

    create: ApplicationSectionSchemaCreate
    update: ApplicationSectionSchemaUpdate
    admin_update: ApplicationSectionSchemaAdminUpdate
    response: ApplicationSectionSchemaResponse
    response_detailed: ApplicationSectionSchemaResponseDetailed

class ApplicationSectionSchemaCreate(AwesomeBaseModel):
    """create schema for ApplicationSection model"""

    application_id: int
    server_type: ServerType
    section_data: dict
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionSchemaUpdate(AwesomeBaseModel):
    """update schema for ApplicationSection model"""

    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionSchemaAdminUpdate(AwesomeBaseModel):
    """admin_update schema for ApplicationSection model"""

    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionSchemaResponse(AwesomeBaseModel):
    """response schema for ApplicationSection model"""

    id: int
    updated_at: datetime
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionSchemaResponseDetailed(AwesomeBaseModel):
    """response_detailed schema for ApplicationSection model"""

    id: int
    updated_at: datetime
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionScopes:
    """Scopes for the ApplicationSection model."""

    create_own: ApplicationSectionScopeCreateOwn
    update_own: ApplicationSectionScopeUpdateOwn
    admin_review: ApplicationSectionScopeAdminReview

class ApplicationSectionScopeCreateOwn(AwesomeBaseModel):
    """create_own schema for ApplicationSection model"""

    id: int
    updated_at: datetime
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionScopeUpdateOwn(AwesomeBaseModel):
    """update_own schema for ApplicationSection model"""

    id: int
    updated_at: datetime
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionScopeAdminReview(AwesomeBaseModel):
    """admin_review schema for ApplicationSection model"""

    id: int
    updated_at: datetime
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    is_required: bool

class ApplicationSectionFilters:
    """Declarative filters for the ApplicationSection model."""

class ApplicationSectionFilter(BaseModel):
    """Pydantic-class for filtering the ApplicationSection model."""

class ApplicationSectionSorts:
    """Declarative sorts for the ApplicationSection model."""

class ApplicationSectionSort(StrEnum):
    """Enum for sorting the ApplicationSection model."""
