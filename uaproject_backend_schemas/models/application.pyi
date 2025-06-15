# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.application import ApplicationStatus
from uaproject_backend_schemas.models.user import User

class Application(AwesomeModel):
    """Base application model."""

    id: int
    updated_at: datetime
    user_id: int
    status: ApplicationStatus
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: List[str]
    user: Optional[User]
    schemas: ApplicationSchemas
    scopes: ApplicationScopes
    filters: ApplicationFilters
    sorts: ApplicationSorts
    filter: type[ApplicationFilter]
    sort: type[ApplicationSort]

class ApplicationSchemas:
    """Schemas for the Application model."""

    create: ApplicationSchemaCreate
    update: ApplicationSchemaUpdate
    update_status: ApplicationSchemaUpdateStatus
    response: ApplicationSchemaResponse
    response_self: ApplicationSchemaResponseSelf

class ApplicationSchemaCreate(AwesomeBaseModel):
    """create schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: List[str]
    user: Optional[User]

class ApplicationSchemaUpdate(AwesomeBaseModel):
    """update schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: List[str]
    user: Optional[User]

class ApplicationSchemaUpdateStatus(AwesomeBaseModel):
    """update_status schema for Application model"""

    status: ApplicationStatus

class ApplicationSchemaResponse(AwesomeBaseModel):
    """response schema for Application model"""

    id: int
    updated_at: datetime
    user_id: int
    status: ApplicationStatus
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: List[str]
    user: Optional[User]

class ApplicationSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for Application model"""

    id: int
    updated_at: datetime
    user_id: int
    status: ApplicationStatus
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: List[str]
    user: Optional[User]

class ApplicationScopes:
    """Scopes for the Application model."""

    status: ApplicationScopeStatus
    editable_fields: ApplicationScopeEditableFields
    form: ApplicationScopeForm

class ApplicationScopeStatus(AwesomeBaseModel):
    """status schema for Application model"""

    id: int
    user_id: int
    status: ApplicationStatus

class ApplicationScopeEditableFields(AwesomeBaseModel):
    """editable_fields schema for Application model"""

    id: int
    user_id: int
    editable_fields: List[str]

class ApplicationScopeForm(AwesomeBaseModel):
    """form schema for Application model"""

    id: int
    user_id: int
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]

class ApplicationFilters:
    """Declarative filters for the Application model."""

class ApplicationFilter(BaseModel):
    """Pydantic-class for filtering the Application model."""

    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    status: Optional[ApplicationStatus] = None
    birth_date: Optional[datetime] = None
    min_birth_date: Optional[Any] = None
    max_birth_date: Optional[Any] = None
    launcher: Optional[str] = None
    server_source: Optional[str] = None
    private_server_experience: Optional[str] = None
    useful_skills: Optional[str] = None
    conflict_reaction: Optional[str] = None
    quiz_answer: Optional[str] = None

class ApplicationSorts:
    """Declarative sorts for the Application model."""

class ApplicationSort(StrEnum):
    """Enum for sorting the Application model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
