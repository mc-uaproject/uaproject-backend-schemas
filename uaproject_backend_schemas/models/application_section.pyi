# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application import Application
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType

class ApplicationSection(AwesomeModel):
    """Base applicationsection model."""

    application: Application
    application_id: int
    id: int
    rejection_reason: Optional[str]
    reviewed_at: Optional[datetime]
    reviewed_by: Optional[int]
    section_data: dict
    server_type: ServerType
    status: ServerAccessStatus
    updated_at: datetime
    schemas: ApplicationSectionSchemas
    scopes: ApplicationSectionScopes
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

    application_id: Optional[int]
    server_type: Optional[ServerType]
    section_data: Optional[dict]
    status: Optional[ServerAccessStatus]
    rejection_reason: Optional[str]
    application: Optional[Application]

class ApplicationSectionSchemaUpdate(AwesomeBaseModel):
    """update schema for ApplicationSection model"""

    section_data: Optional[dict]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Optional[Application]

class ApplicationSectionSchemaAdminUpdate(AwesomeBaseModel):
    """admin_update schema for ApplicationSection model"""

    server_type: Optional[ServerType]
    section_data: Optional[dict]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Optional[Application]

class ApplicationSectionSchemaResponse(AwesomeBaseModel):
    """response schema for ApplicationSection model"""

    updated_at: datetime
    id: int
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Application

class ApplicationSectionSchemaResponseDetailed(AwesomeBaseModel):
    """response_detailed schema for ApplicationSection model"""

    updated_at: datetime
    id: int
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Application

class ApplicationSectionScopes:
    """Scopes for the ApplicationSection model."""

    create_own: ApplicationSectionScopeCreateOwn
    update_own: ApplicationSectionScopeUpdateOwn
    admin_review: ApplicationSectionScopeAdminReview

class ApplicationSectionScopeCreateOwn(AwesomeBaseModel):
    """create_own schema for ApplicationSection model"""

    updated_at: datetime
    id: int
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Application

class ApplicationSectionScopeUpdateOwn(AwesomeBaseModel):
    """update_own schema for ApplicationSection model"""

    updated_at: datetime
    id: int
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Application

class ApplicationSectionScopeAdminReview(AwesomeBaseModel):
    """admin_review schema for ApplicationSection model"""

    updated_at: datetime
    id: int
    application_id: int
    server_type: ServerType
    section_data: dict
    status: ServerAccessStatus
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    application: Application

class ApplicationSectionFilter(BaseModel):
    """Pydantic-class for filtering the ApplicationSection model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    application_id: Optional[int] = None
    min_application_id: Optional[Any] = None
    max_application_id: Optional[Any] = None
    server_type: Optional[ServerType] = None
    section_data: Optional[dict] = None
    status: Optional[ServerAccessStatus] = None
    reviewed_by: Optional[int] = None
    min_reviewed_by: Optional[Any] = None
    max_reviewed_by: Optional[Any] = None
    reviewed_at: Optional[datetime] = None
    min_reviewed_at: Optional[Any] = None
    max_reviewed_at: Optional[Any] = None
    rejection_reason: Optional[str] = None

class ApplicationSectionSort(StrEnum):
    """Enum for sorting the ApplicationSection model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
