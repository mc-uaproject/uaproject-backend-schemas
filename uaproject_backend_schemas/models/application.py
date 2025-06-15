from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import model_validator
from sqlmodel import ARRAY, BigInteger, Column, Enum, ForeignKey, Relationship, String

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition
from uaproject_backend_schemas.models.schemas.application import ApplicationStatus
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.application_section import ApplicationSection
    from uaproject_backend_schemas.models.user import User

# Legacy fields (v1)
LEGACY_EDITABLE_FIELDS: List[str] = [
    "birth_date",
    "launcher",
    "server_source",
    "private_server_experience",
    "useful_skills",
    "conflict_reaction",
    "quiz_answer",
]

SURVIVAL_LEVEL_FIELDS: List[str] = [
    "birth_date",
    "launcher",
    "server_source",
    "minecraft_experience_years",
    "preferred_gamemode",
    "russian_word_reaction",
    "griefing_rule_attitude",
    "chat_conflict_handling",
    "admin_decision_attitude",
    "new_rule_reaction",
    "useful_skills_detailed",
    "portfolio_links",
    "server_experience_positive",
    "server_experience_negative",
    "creeper_explosion_reaction",
    "incomplete_tree_reaction",
    "neighbor_proximity_reaction",
]

EVERVAULT_LEVEL_FIELDS: List[str] = [
    "permanent_world_attitude",
    "long_project_experience",
    "community_projects_readiness",
    "vanilla_experience_preference",
    "ideal_server_description",
    "healthy_community_definition",
]

DEFAULT_EDITABLE_FIELDS: List[str] = SURVIVAL_LEVEL_FIELDS + EVERVAULT_LEVEL_FIELDS


class Application(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    __tablename__ = "applications"
    __scope_prefix__ = "application"
    model_config = {"arbitrary_types_allowed": True}

    # Core fields
    user_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False, unique=True)
    )
    version: str = AwesomeField(default="v2", max_length=10, description="Application version")
    status: ApplicationStatus = AwesomeField(
        sa_column=Column(
            Enum(ApplicationStatus, native_enum=False),
            default=ApplicationStatus.NOT_SENT.value,
            server_default=ApplicationStatus.NOT_SENT.value,
        )
    )

    # Base fields (always present)
    birth_date: Optional[datetime] = AwesomeField(nullable=True)
    launcher: Optional[str] = AwesomeField(max_length=32, nullable=True)
    server_source: Optional[str] = AwesomeField(max_length=512, nullable=True)

    # Legacy v1 fields (for backward compatibility)
    private_server_experience: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Legacy v1 field"
    )
    useful_skills: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Legacy v1 field"
    )
    conflict_reaction: Optional[str] = AwesomeField(max_length=1024, nullable=True)
    quiz_answer: Optional[str] = AwesomeField(max_length=1024, nullable=True)

    # Survival level questions (first level)
    russian_word_reaction: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Reaction to using Russian words in chat"
    )
    griefing_rule_attitude: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Attitude towards griefing rule 2.3"
    )
    chat_conflict_handling: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="How to handle conflicts in chat"
    )
    admin_decision_attitude: Optional[str] = AwesomeField(
        max_length=2048,
        nullable=True,
        description="Attitude towards admin discretion in punishments",
    )
    new_rule_reaction: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Reaction to new rules you don't like"
    )
    useful_skills_detailed: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Detailed description of useful skills"
    )
    portfolio_links: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Links to portfolio work (optional)"
    )
    server_experience_positive: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Positive experience on other servers"
    )
    server_experience_negative: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Negative experience on other servers"
    )

    # Evervault level questions (second level)
    permanent_world_attitude: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Attitude towards permanent world without wipes"
    )
    long_project_experience: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Experience with long-term Minecraft projects"
    )
    community_projects_readiness: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Readiness to participate in community projects"
    )
    vanilla_experience_preference: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Preference for vanilla survival experience"
    )
    ideal_server_description: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Description of ideal Minecraft server"
    )
    healthy_community_definition: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Definition of healthy gaming community"
    )

    # Additional questions
    creeper_explosion_reaction: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Actions when creeper explodes near you"
    )
    incomplete_tree_reaction: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Reaction to new player leaving incomplete tree"
    )
    neighbor_proximity_reaction: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Actions when finding neighbor living nearby"
    )

    editable_fields: List[str] = AwesomeField(
        sa_column=Column(
            ARRAY(String),
            nullable=False,
            default=DEFAULT_EDITABLE_FIELDS,
            server_default="{}",
        )
    )

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="application", sa_relationship_kwargs={"uselist": False}
    )
    sections: List["ApplicationSection"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[ApplicationSection.application_id]",
            "cascade": "all, delete-orphan",
        }
    )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "user_id", "status", "version"]
            optional = True
            permissions = [".write.self"]

        class Update(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "user_id", "status", "version"]
            optional = True
            permissions = [".write.self"]

        class UpdateStatus(SchemaDefinition):
            fields = ["status"]
            permissions = [".admin"]

        class Response(SchemaDefinition):
            permissions = [".read.other"]

        class ResponseSelf(SchemaDefinition):
            permissions = [".read.self"]

        class ResponseWithSections(SchemaDefinition):
            """Response with server sections included."""

            permissions = [".read.self"]

        class CreateV2(SchemaDefinition):
            """Schema for v2 applications with new fields."""

            fields_exclude = [
                "id",
                "created_at",
                "updated_at",
                "user_id",
                "status",
                "version",
                "private_server_experience",
                "useful_skills",
            ]  # exclude legacy fields
            optional = True
            permissions = [".write.self"]

        class CreateSurvival(SchemaDefinition):
            """Schema for survival level application (first level)."""

            fields_include = SURVIVAL_LEVEL_FIELDS
            optional = True
            permissions = [".write.self"]

        class CreateEvervault(SchemaDefinition):
            """Schema for evervault level application (second level)."""

            fields_include = EVERVAULT_LEVEL_FIELDS
            optional = True
            permissions = [".write.self"]

        class UpdateSurvival(SchemaDefinition):
            """Schema for updating survival level fields."""

            fields_include = SURVIVAL_LEVEL_FIELDS
            optional = True
            permissions = [".write.self"]

        class UpdateEvervault(SchemaDefinition):
            """Schema for updating evervault level fields."""

            fields_include = EVERVAULT_LEVEL_FIELDS
            optional = True
            permissions = [".write.self"]

    class Scopes(AwesomeModel.Scopes):
        class Status(ScopeDefinition):
            trigger_fields = ["status"]
            fields = ["id", "user_id", "status"]
            permissions = ["read"]

        class EditableFields(ScopeDefinition):
            trigger_fields = ["editable_fields"]
            fields = ["id", "user_id", "editable_fields"]
            permissions = ["read"]

        class Form(ScopeDefinition):
            trigger_fields = DEFAULT_EDITABLE_FIELDS
            fields = ["id", "user_id", *DEFAULT_EDITABLE_FIELDS]
            permissions = ["read"]

    @model_validator(mode="before")
    def validate_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        # Legacy fields validation
        for field in [
            "private_server_experience",
            "useful_skills",
            "conflict_reaction",
            "quiz_answer",
        ]:
            cls._validate_text_length(field, values.get(field))

        # New application fields validation (minimum 20 words)
        min_length_fields = [
            "russian_word_reaction",
            "griefing_rule_attitude",
            "chat_conflict_handling",
            "admin_decision_attitude",
            "new_rule_reaction",
            "useful_skills_detailed",
            "server_experience_positive",
            "server_experience_negative",
            "permanent_world_attitude",
            "long_project_experience",
            "community_projects_readiness",
            "vanilla_experience_preference",
            "ideal_server_description",
            "healthy_community_definition",
        ]

        for field in min_length_fields:
            value = values.get(field)
            if value and isinstance(value, str):
                word_count = len(value.split())
                if word_count < 20:
                    raise ValueError(
                        f"{field} must contain at least 20 words (current: {word_count})"
                    )

        if editable_fields := values.get("editable_fields"):
            if not isinstance(editable_fields, list):
                raise ValueError("Editable fields must be a list")
            if not all(field in cls.DEFAULT_EDITABLE_FIELDS for field in editable_fields):
                raise ValueError("Invalid editable fields")

        return values

    # Helper methods for server access management
    def get_section(self, server_type: ServerType) -> Optional["ApplicationSection"]:
        """Get section for specific server type."""
        return next((s for s in self.sections if s.server_type == server_type), None)

    def get_server_access_status(self, server_type: ServerType) -> ServerAccessStatus:
        """Get access status for specific server."""
        section = self.get_section(server_type)
        return section.status if section else ServerAccessStatus.NOT_APPLIED

    def get_accessible_servers(self) -> List[ServerType]:
        """Get list of servers user has access to."""
        return [s.server_type for s in self.sections if s.status == ServerAccessStatus.APPROVED]

    def get_pending_servers(self) -> List[ServerType]:
        """Get list of servers with pending applications."""
        return [s.server_type for s in self.sections if s.status == ServerAccessStatus.PENDING]

    def get_rejected_servers(self) -> List[ServerType]:
        """Get list of servers with rejected applications."""
        return [s.server_type for s in self.sections if s.status == ServerAccessStatus.REJECTED]

    def can_access_server(self, server_type: ServerType) -> bool:
        """Check if user can access specific server."""
        return self.get_server_access_status(server_type) == ServerAccessStatus.APPROVED

    def get_available_servers_to_apply(self) -> List[ServerType]:
        """Get list of servers user can still apply to."""
        applied_servers = {s.server_type for s in self.sections}
        return [server for server in ServerType if server not in applied_servers]

    def get_server_access_summary(self) -> Dict[str, Any]:
        """Get comprehensive server access summary."""
        return {
            "accessible_servers": [s.value for s in self.get_accessible_servers()],
            "pending_servers": [s.value for s in self.get_pending_servers()],
            "rejected_servers": [s.value for s in self.get_rejected_servers()],
            "available_to_apply": [s.value for s in self.get_available_servers_to_apply()],
            "overall_status": self._get_overall_access_status(),
        }

    def _get_overall_access_status(self) -> str:
        """Get overall access status description."""
        accessible = self.get_accessible_servers()
        rejected = self.get_rejected_servers()
        pending = self.get_pending_servers()

        if not self.sections:
            return "no_applications"
        elif accessible and not rejected and not pending:
            return "full_access"
        elif accessible:
            return "partial_access"
        elif rejected and not accessible and not pending:
            return "all_rejected"
        else:
            return "under_review"
