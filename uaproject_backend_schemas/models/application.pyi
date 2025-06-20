# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.application_section import ApplicationSection
from uaproject_backend_schemas.models.schemas.application import ApplicationStatus
from uaproject_backend_schemas.models.user import User

class Application(AwesomeModel):
    """Base application model."""

    id: int
    updated_at: datetime
    user_id: int
    version: str
    status: ApplicationStatus
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    griefing_rule_attitude: Optional[str]
    chat_conflict_handling: Optional[str]
    portfolio_links: Optional[str]
    server_experience_positive: Optional[str]
    permanent_world_attitude: Optional[str]
    vanilla_experience_preference: Optional[str]
    creeper_explosion_reaction: Optional[str]
    incomplete_tree_reaction: Optional[str]
    neighbor_proximity_reaction: Optional[str]
    editable_fields: List[str]
    created_at: datetime
    user: Optional[User]
    sections: Optional[List[ApplicationSection]]
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

class ApplicationSchemaCreate(AwesomeBaseModel):
    """create schema for Application model"""

    id: int

class ApplicationSchemaUpdate(AwesomeBaseModel):
    """update schema for Application model"""

    status: ApplicationStatus
    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    private_server_experience: Optional[str]
    useful_skills: Optional[str]
    conflict_reaction: Optional[str]
    quiz_answer: Optional[str]
    griefing_rule_attitude: Optional[str]
    chat_conflict_handling: Optional[str]
    portfolio_links: Optional[str]
    server_experience_positive: Optional[str]
    permanent_world_attitude: Optional[str]
    vanilla_experience_preference: Optional[str]
    creeper_explosion_reaction: Optional[str]
    incomplete_tree_reaction: Optional[str]
    neighbor_proximity_reaction: Optional[str]
    editable_fields: List[str]
    user: Optional[User]
    sections: Optional[List[ApplicationSection]]

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
    minecraft_experience_years: Any
    preferred_gamemode: Any
    griefing_rule_attitude: Optional[str]
    chat_conflict_handling: Optional[str]
    portfolio_links: Optional[str]
    server_experience_positive: Optional[str]
    creeper_explosion_reaction: Optional[str]
    incomplete_tree_reaction: Optional[str]
    neighbor_proximity_reaction: Optional[str]

class ApplicationSchemaCreateEvervault(AwesomeBaseModel):
    """create_evervault schema for Application model"""

    birth_date: Optional[datetime]
    launcher: Optional[str]
    server_source: Optional[str]
    minecraft_experience_years: Any
    preferred_gamemode: Any
    griefing_rule_attitude: Optional[str]
    chat_conflict_handling: Optional[str]
    portfolio_links: Optional[str]
    server_experience_positive: Optional[str]
    creeper_explosion_reaction: Optional[str]
    incomplete_tree_reaction: Optional[str]
    neighbor_proximity_reaction: Optional[str]
    permanent_world_attitude: Optional[str]
    vanilla_experience_preference: Optional[str]

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
    minecraft_experience_years: Any
    preferred_gamemode: Any
    griefing_rule_attitude: Optional[str]
    chat_conflict_handling: Optional[str]
    portfolio_links: Optional[str]
    server_experience_positive: Optional[str]
    creeper_explosion_reaction: Optional[str]
    incomplete_tree_reaction: Optional[str]
    neighbor_proximity_reaction: Optional[str]
    permanent_world_attitude: Optional[str]
    vanilla_experience_preference: Optional[str]

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
    griefing_rule_attitude: Optional[str] = None
    chat_conflict_handling: Optional[str] = None
    portfolio_links: Optional[str] = None
    server_experience_positive: Optional[str] = None
    permanent_world_attitude: Optional[str] = None
    vanilla_experience_preference: Optional[str] = None
    creeper_explosion_reaction: Optional[str] = None
    incomplete_tree_reaction: Optional[str] = None
    neighbor_proximity_reaction: Optional[str] = None
    sections_id: Optional[Any] = None

class ApplicationSort(StrEnum):
    """Enum for sorting the Application model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
