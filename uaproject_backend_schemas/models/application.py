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
    "griefing_rule_attitude",
    "chat_conflict_handling",
    "portfolio_links",
    "server_experience_positive",
    "creeper_explosion_reaction",
    "incomplete_tree_reaction",
    "neighbor_proximity_reaction",
]

EVERVAULT_LEVEL_FIELDS: List[str] = [
    "permanent_world_attitude",
    "vanilla_experience_preference",
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
    griefing_rule_attitude: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Attitude towards griefing rule 2.3"
    )
    chat_conflict_handling: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="How to handle conflicts in chat"
    )
    portfolio_links: Optional[str] = AwesomeField(
        max_length=1024, nullable=True, description="Links to portfolio work (optional)"
    )
    server_experience_positive: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Positive experience on other servers"
    )

    # Evervault level questions (second level)
    permanent_world_attitude: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Attitude towards permanent world without wipes"
    )
    vanilla_experience_preference: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Preference for vanilla survival experience"
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
            server_default="{}",
        ),
        default_factory=lambda: LEGACY_EDITABLE_FIELDS.copy(),
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
            """Default create schema - requires only essential fields, makes legacy fields optional."""

            fields = ["id"]
            optional = True
            permissions = [".write.self"]

        class Update(SchemaDefinition):
            """Default update schema - excludes system fields."""

            fields_exclude = [
                "id",
                "created_at",
                "updated_at",
                "user_id",
                "version",
            ]
            optional = True
            permissions = [".admin"]

        class CreateLegacy(SchemaDefinition):
            """Schema for creating legacy v1 applications."""

            fields = LEGACY_EDITABLE_FIELDS
            optional = True
            permissions = [".write.self"]

        class CreateV2(SchemaDefinition):
            """Schema for creating v2 applications with survival level questions."""

            fields = SURVIVAL_LEVEL_FIELDS
            optional = True
            permissions = [".write.self"]

        class CreateEvervault(SchemaDefinition):
            """Schema for creating evervault applications with all questions."""

            fields = DEFAULT_EDITABLE_FIELDS
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

    @model_validator(mode="after")
    def validate_fields(self):
        # Auto-set version based on editable_fields
        if set(self.editable_fields) == set(LEGACY_EDITABLE_FIELDS):
            self.version = "v1"
        elif set(self.editable_fields) >= set(DEFAULT_EDITABLE_FIELDS):
            self.version = "v2"

        min_length_fields = [
            "griefing_rule_attitude",
            "chat_conflict_handling",
            "server_experience_positive",
            "permanent_world_attitude",
            "vanilla_experience_preference",
        ]

        for field in min_length_fields:
            value = getattr(self, field, None)
            if value and isinstance(value, str):
                word_count = len(value.split())
                if word_count < 20:
                    raise ValueError(
                        f"{field} must contain at least 20 words (current: {word_count})"
                    )

        return self

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
