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
    created_at: datetime
    id: int
    rejection_reason: Optional[str]
    reviewed_at: Optional[datetime]
    reviewed_by: Optional[int]
    section_data: dict
    server_type: ServerType
    status: ServerAccessStatus
    updated_at: datetime
    schemas: ApplicationSectionSchemas
    filter: type[ApplicationSectionFilter]
    sort: type[ApplicationSectionSort]

class ApplicationSectionSchemas:
    """Schemas for the ApplicationSection model."""

    admin_update: ApplicationSectionSchemaAdminUpdate
    create: ApplicationSectionSchemaCreate
    redis: ApplicationSectionSchemaRedis
    response: ApplicationSectionSchemaResponse
    response_detailed: ApplicationSectionSchemaResponseDetailed
    update: ApplicationSectionSchemaUpdate

class ApplicationSectionSchemaAdminUpdate(AwesomeBaseModel):
    """admin_update schema for ApplicationSection model"""

    status: Optional[ServerAccessStatus]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    server_type: Optional[ServerType]
    section_data: Optional[dict]
    reviewed_by: Optional[int]

class ApplicationSectionSchemaCreate(AwesomeBaseModel):
    """create schema for ApplicationSection model"""

    status: Optional[ServerAccessStatus]
    application_id: Optional[int]
    rejection_reason: Optional[str]
    server_type: Optional[ServerType]
    section_data: Optional[dict]

class ApplicationSectionSchemaRedis(AwesomeBaseModel):
    """redis schema for ApplicationSection model"""

    status: Optional[ServerAccessStatus]
    application_id: Optional[int]
    application: Optional[Application]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    server_type: Optional[ServerType]
    updated_at: Optional[datetime]
    section_data: Optional[dict]
    created_at: Optional[datetime]
    id: Optional[int]
    reviewed_by: Optional[int]

class ApplicationSectionSchemaResponse(AwesomeBaseModel):
    """response schema for ApplicationSection model"""

    status: Optional[ServerAccessStatus]
    application_id: int
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    server_type: ServerType
    updated_at: Optional[datetime]
    section_data: Optional[dict]
    created_at: Optional[datetime]
    id: Optional[int]
    reviewed_by: Optional[int]

class ApplicationSectionSchemaResponseDetailed(AwesomeBaseModel):
    """response_detailed schema for ApplicationSection model"""

    status: Optional[ServerAccessStatus]
    application_id: int
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    server_type: ServerType
    updated_at: Optional[datetime]
    section_data: Optional[dict]
    created_at: Optional[datetime]
    id: Optional[int]
    reviewed_by: Optional[int]

class ApplicationSectionSchemaUpdate(AwesomeBaseModel):
    """update schema for ApplicationSection model"""

    status: Optional[ServerAccessStatus]
    reviewed_at: Optional[datetime]
    rejection_reason: Optional[str]
    section_data: Optional[dict]
    reviewed_by: Optional[int]

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
