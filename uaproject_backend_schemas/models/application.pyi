# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

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
    created_at: datetime
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
    filter: type[ApplicationFilter]
    sort: type[ApplicationSort]

class ApplicationSchemas:
    """Schemas for the Application model."""

    create: ApplicationSchemaCreate
    create_base: ApplicationSchemaCreateBase
    create_evervault: ApplicationSchemaCreateEvervault
    create_legacy: ApplicationSchemaCreateLegacy
    create_v2: ApplicationSchemaCreateV2
    redis: ApplicationSchemaRedis
    response: ApplicationSchemaResponse
    update: ApplicationSchemaUpdate

class ApplicationSchemaCreate(AwesomeBaseModel):
    """create schema for Application model"""

    server_source: Optional[str]
    birth_date: Optional[datetime]
    new_rule_reaction: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    private_server_experience: Optional[str]
    useful_skills_detailed: Optional[str]
    conflict_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    server_experience_negative: Optional[str]
    useful_skills: Optional[str]
    healthy_community_definition: Optional[str]
    user_id: Optional[int]
    russian_word_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: Optional[list[str]]
    launcher: Optional[str]
    ideal_server_description: Optional[str]
    version: Optional[str]
    created_at: datetime

class ApplicationSchemaCreateBase(AwesomeBaseModel):
    """create_base schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    created_at: datetime

class ApplicationSchemaCreateEvervault(AwesomeBaseModel):
    """create_evervault schema for Application model"""

    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    healthy_community_definition: Optional[str]
    ideal_server_description: Optional[str]
    created_at: datetime

class ApplicationSchemaCreateLegacy(AwesomeBaseModel):
    """create_legacy schema for Application model"""

    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    created_at: datetime

class ApplicationSchemaCreateV2(AwesomeBaseModel):
    """create_v2 schema for Application model"""

    russian_word_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    new_rule_reaction: Optional[str]
    useful_skills_detailed: Optional[str]
    server_experience_negative: Optional[str]
    created_at: datetime

class ApplicationSchemaRedis(AwesomeBaseModel):
    """redis schema for Application model"""

    server_source: Optional[str]
    sections: Optional[list[ApplicationSection]]
    birth_date: Optional[datetime]
    new_rule_reaction: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    private_server_experience: Optional[str]
    useful_skills_detailed: Optional[str]
    conflict_reaction: Optional[str]
    id: Optional[int]
    admin_decision_attitude: Optional[str]
    server_experience_negative: Optional[str]
    useful_skills: Optional[str]
    healthy_community_definition: Optional[str]
    user_id: Optional[int]
    russian_word_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: Optional[list[str]]
    launcher: Optional[str]
    updated_at: Optional[datetime]
    ideal_server_description: Optional[str]
    version: Optional[str]
    user: Optional[User]
    created_at: datetime

class ApplicationSchemaResponse(AwesomeBaseModel):
    """response schema for Application model"""

    server_source: Optional[str]
    birth_date: Optional[datetime]
    new_rule_reaction: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    private_server_experience: Optional[str]
    useful_skills_detailed: Optional[str]
    conflict_reaction: Optional[str]
    id: Optional[int]
    admin_decision_attitude: Optional[str]
    server_experience_negative: Optional[str]
    useful_skills: Optional[str]
    healthy_community_definition: Optional[str]
    user_id: int
    russian_word_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: Optional[list[str]]
    launcher: Optional[str]
    updated_at: Optional[datetime]
    ideal_server_description: Optional[str]
    version: Optional[str]
    created_at: datetime

class ApplicationSchemaUpdate(AwesomeBaseModel):
    """update schema for Application model"""

    server_source: Optional[str]
    birth_date: Optional[datetime]
    new_rule_reaction: Optional[str]
    long_project_experience: Optional[str]
    community_projects_readiness: Optional[str]
    private_server_experience: Optional[str]
    useful_skills_detailed: Optional[str]
    conflict_reaction: Optional[str]
    admin_decision_attitude: Optional[str]
    server_experience_negative: Optional[str]
    useful_skills: Optional[str]
    healthy_community_definition: Optional[str]
    russian_word_reaction: Optional[str]
    quiz_answer: Optional[str]
    editable_fields: Optional[list[str]]
    launcher: Optional[str]
    ideal_server_description: Optional[str]
    created_at: datetime

class ApplicationFilter(BaseModel):
    """Pydantic-class for filtering the Application model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    version: Optional[str] = None
    birth_date: Optional[datetime] = None
    min_birth_date: Optional[datetime] = None
    max_birth_date: Optional[datetime] = None
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
    sections_id: Optional[int] = None

class ApplicationSort(StrEnum):
    """Enum for sorting the Application model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
