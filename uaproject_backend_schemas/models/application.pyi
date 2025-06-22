# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application_section import ApplicationSection
from uaproject_backend_schemas.models.user import User

class Application(AwesomeModel):
    """Base application model."""

    admin_decision_attitude: Optional[str]
    birth_date: Optional[datetime]
    community_projects_readiness: Optional[str]
    conflict_reaction: Optional[str]
    editable_fields: list[str]
    healthy_community_definition: Optional[str]
    id: int
    ideal_server_description: Optional[str]
    launcher: Optional[str]
    long_project_experience: Optional[str]
    new_rule_reaction: Optional[str]
    private_server_experience: Optional[str]
    quiz_answer: Optional[str]
    russian_word_reaction: Optional[str]
    sections: list[ApplicationSection]
    server_experience_negative: Optional[str]
    server_source: Optional[str]
    updated_at: datetime
    useful_skills: Optional[str]
    useful_skills_detailed: Optional[str]
    user: Optional[User]
    user_id: int
    version: str
    schemas: ApplicationSchemas
    scopes: ApplicationScopes
    filter: type[ApplicationFilter]
    sort: type[ApplicationSort]

class ApplicationSchemas:
    """Schemas for the Application model."""

    create: ApplicationSchemaCreate
    update: ApplicationSchemaUpdate
    create_legacy: ApplicationSchemaCreateLegacy
    create_v2: ApplicationSchemaCreateV2
    create_evervault: ApplicationSchemaCreateEvervault
    response: ApplicationSchemaResponse

class ApplicationSchemaCreate(AwesomeBaseModel):
    """create schema for Application model"""

    user_id: Optional[int]
    version: Optional[str]
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    russian_word_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    new_rule_reaction: Optional[str]
    useful_skills_detailed: Optional[str]
    server_experience_negative: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    healthy_community_definition: Optional[str]
    ideal_server_description: Optional[str]
    editable_fields: Optional[list[str]]
    user: Optional[User]
    sections: Optional[list[ApplicationSection]]

class ApplicationSchemaUpdate(AwesomeBaseModel):
    """update schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    russian_word_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    new_rule_reaction: Optional[str]
    useful_skills_detailed: Optional[str]
    server_experience_negative: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    healthy_community_definition: Optional[str]
    ideal_server_description: Optional[str]
    editable_fields: Optional[list[str]]
    user: Optional[User]
    sections: Optional[list[ApplicationSection]]

class ApplicationSchemaCreateLegacy(AwesomeBaseModel):
    """create_legacy schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]

class ApplicationSchemaCreateV2(AwesomeBaseModel):
    """create_v2 schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    russian_word_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    new_rule_reaction: Optional[str]
    useful_skills_detailed: Optional[str]
    server_experience_negative: Optional[str]

class ApplicationSchemaCreateEvervault(AwesomeBaseModel):
    """create_evervault schema for Application model"""

    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    healthy_community_definition: Optional[str]
    ideal_server_description: Optional[str]

class ApplicationSchemaResponse(AwesomeBaseModel):
    """response schema for Application model"""

    id: int
    updated_at: datetime
    user_id: int
    version: str
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    russian_word_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    new_rule_reaction: Optional[str]
    useful_skills_detailed: Optional[str]
    server_experience_negative: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    healthy_community_definition: Optional[str]
    ideal_server_description: Optional[str]
    editable_fields: list[str]
    user: Optional[User]
    sections: list[ApplicationSection]

class ApplicationScopes:
    """Scopes for the Application model."""

    editable_fields: ApplicationScopeEditableFields
    form: ApplicationScopeForm

class ApplicationScopeEditableFields(AwesomeBaseModel):
    """editable_fields schema for Application model"""

    id: int
    user_id: int
    editable_fields: list[str]

class ApplicationScopeForm(AwesomeBaseModel):
    """form schema for Application model"""

    id: int
    user_id: int
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    russian_word_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    new_rule_reaction: Optional[str]
    useful_skills_detailed: Optional[str]
    server_experience_negative: Optional[str]

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
    version: Optional[str] = None
    birth_date: Optional[datetime] = None
    min_birth_date: Optional[Any] = None
    max_birth_date: Optional[Any] = None
    launcher: Optional[str] = None
    server_source: Optional[str] = None
    private_server_experience: Optional[str] = None
    useful_skills: Optional[str] = None
    conflict_reaction: Optional[str] = None
    quiz_answer: Optional[str] = None
    russian_word_reaction: Optional[str] = None
    admin_decision_attitude: Optional[str] = None
    new_rule_reaction: Optional[str] = None
    useful_skills_detailed: Optional[str] = None
    server_experience_negative: Optional[str] = None
    long_project_experience: Optional[str] = None
    community_projects_readiness: Optional[str] = None
    healthy_community_definition: Optional[str] = None
    ideal_server_description: Optional[str] = None

class ApplicationSort(StrEnum):
    """Enum for sorting the Application model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
