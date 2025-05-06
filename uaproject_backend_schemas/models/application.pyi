# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import List, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.application import ApplicationStatus

class Application(AwesomeModel):
    """Base user model."""

    schemas: ApplicationSchemas
    scopes: ApplicationScopes

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
