# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.application import ApplicationStatus
from uaproject_backend_schemas.models.user import User

class Application(AwesomeModel):
    """Base user model."""

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
    filter: type[ApplicationFilter]

class ApplicationSchemas:
    """Schemas for the user model."""

    create: ApplicationSchemaCreate
    update: ApplicationSchemaUpdate
    response: ApplicationSchemaResponse

class ApplicationScopes:
    """Visibility scopes for the user model."""

    status: ApplicationScopeStatus
    editable_fields: ApplicationScopeEditableFields
    form: ApplicationScopeForm
    full: ApplicationScopeFull

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
    editable_fields: Optional[List] = None

class ApplicationSchemaCreate(AwesomeBaseModel):
    """Create schema for Application model"""

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

class ApplicationSchemaUpdate(AwesomeBaseModel):
    """Update schema for Application model"""

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

class ApplicationSchemaResponse(AwesomeBaseModel):
    """Response schema for Application model"""

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

class ApplicationScopeStatus(AwesomeBaseModel):
    """status visibility scope for Application model"""

    id: int
    user_id: int
    status: ApplicationStatus

class ApplicationScopeEditableFields(AwesomeBaseModel):
    """editable_fields visibility scope for Application model"""

    id: int
    user_id: int
    editable_fields: List[str]

class ApplicationScopeForm(AwesomeBaseModel):
    """form visibility scope for Application model"""

    id: int
    user_id: int
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]

class ApplicationScopeFull(AwesomeBaseModel):
    """full visibility scope for Application model"""

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
