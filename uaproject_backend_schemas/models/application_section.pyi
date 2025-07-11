# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

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

    reviewed_at: Optional[datetime]
    section_data: Optional[dict]
    server_type: Optional[ServerType]
    rejection_reason: Optional[str]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]

class ApplicationSectionSchemaCreate(AwesomeBaseModel):
    """create schema for ApplicationSection model"""

    section_data: Optional[dict]
    server_type: Optional[ServerType]
    rejection_reason: Optional[str]
    application_id: Optional[int]
    status: Optional[ServerAccessStatus]

class ApplicationSectionSchemaRedis(AwesomeBaseModel):
    """redis schema for ApplicationSection model"""

    reviewed_at: Optional[datetime]
    section_data: Optional[dict]
    server_type: Optional[ServerType]
    rejection_reason: Optional[str]
    updated_at: Optional[datetime]
    application_id: Optional[int]
    application: Optional[Application]
    id: Optional[int]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]
    created_at: datetime

class ApplicationSectionSchemaResponse(AwesomeBaseModel):
    """response schema for ApplicationSection model"""

    reviewed_at: Optional[datetime]
    section_data: Optional[dict]
    server_type: ServerType
    rejection_reason: Optional[str]
    updated_at: Optional[datetime]
    application_id: int
    id: Optional[int]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]
    created_at: datetime

class ApplicationSectionSchemaResponseDetailed(AwesomeBaseModel):
    """response_detailed schema for ApplicationSection model"""

    reviewed_at: Optional[datetime]
    section_data: Optional[dict]
    server_type: ServerType
    rejection_reason: Optional[str]
    updated_at: Optional[datetime]
    application_id: int
    id: Optional[int]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]
    created_at: datetime

class ApplicationSectionSchemaUpdate(AwesomeBaseModel):
    """update schema for ApplicationSection model"""

    reviewed_at: Optional[datetime]
    section_data: Optional[dict]
    rejection_reason: Optional[str]
    status: Optional[ServerAccessStatus]
    reviewed_by: Optional[int]

class ApplicationSectionFilter(BaseModel):
    """Pydantic-class for filtering the ApplicationSection model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    application_id: Optional[int] = None
    min_application_id: Optional[int] = None
    max_application_id: Optional[int] = None
    server_type: Optional[ServerType] = None
    section_data: Optional[dict] = None
    status: Optional[ServerAccessStatus] = None
    reviewed_by: Optional[int] = None
    min_reviewed_by: Optional[int] = None
    max_reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    min_reviewed_at: Optional[datetime] = None
    max_reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

class ApplicationSectionSort(StrEnum):
    """Enum for sorting the ApplicationSection model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
