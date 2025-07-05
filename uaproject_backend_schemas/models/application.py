from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import model_validator
from sqlmodel import ARRAY, BigInteger, Column, ForeignKey, Index, Relationship, String

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.application_section import ApplicationSection
    from uaproject_backend_schemas.models.user import User

# Legacy fields (v1) - keeping for backward compatibility
LEGACY_EDITABLE_FIELDS: List[str] = [
    "birth_date",
    "launcher",
    "server_source",
    "private_server_experience",
    "useful_skills",
    "conflict_reaction",
    "quiz_answer",
]

# V2 fields - simplified set
V2_EDITABLE_FIELDS: List[str] = [
    "birth_date",
    "launcher",
    "server_source",
    "russian_word_reaction",
    "admin_decision_attitude",
    "new_rule_reaction",
    "useful_skills_detailed",
    "server_experience_negative",
]

# All editable fields combined
DEFAULT_EDITABLE_FIELDS: List[str] = V2_EDITABLE_FIELDS
EVERVAULT_EDITABLE_FIELDS = [
    "long_project_experience",
    "community_projects_readiness",
    "healthy_community_definition",
    "ideal_server_description",
]


class Application(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "applications"
    __scope_prefix__ = "application"
    __table_args__ = (
        Index("ix_applications_user_id", "user_id"),
        Index("ix_applications_version", "version"),
    )
    # Core fields
    user_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False, unique=True)
    )
    version: str = AwesomeField(default="v2", max_length=10, description="Application version")
    # REMOVED: status field - moved to ApplicationSection

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

    # V2 fields
    russian_word_reaction: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Reaction to hearing 'привет' on server"
    )
    admin_decision_attitude: Optional[str] = AwesomeField(
        max_length=2048,
        nullable=True,
        description="Attitude towards admin decisions and punishments",
    )
    new_rule_reaction: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Reaction to new rules or mechanics"
    )
    useful_skills_detailed: Optional[str] = AwesomeField(
        max_length=2048,
        nullable=True,
        description="Detailed description of useful skills outside Minecraft",
    )
    server_experience_negative: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Negative experience on other servers"
    )

    # Evervault fields
    long_project_experience: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Experience with long-term projects"
    )
    community_projects_readiness: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Readiness for community projects"
    )
    healthy_community_definition: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Definition of healthy community"
    )
    ideal_server_description: Optional[str] = AwesomeField(
        max_length=2048, nullable=True, description="Description of ideal server"
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

            fields_exclude = ["id", "created_at", "updated_at"]
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
            fields_exclude = ["id", "created_at", "updated_at"]
            optional = True
            permissions = [".write.self"]

        class CreateV2(SchemaDefinition):
            """Schema for creating v2 applications."""

            fields = V2_EDITABLE_FIELDS
            fields_exclude = ["id", "created_at", "updated_at"]
            optional = True
            permissions = [".write.self"]

        class CreateEvervault(SchemaDefinition):
            """Schema for creating evervault applications."""

            fields = EVERVAULT_EDITABLE_FIELDS
            fields_exclude = ["id", "created_at", "updated_at"]
            optional = True
            permissions = [".write.self"]

        class Response(SchemaDefinition):
            permissions = [".read"]

    @model_validator(mode="after")
    def validate_fields(self):
        # Auto-set version based on editable_fields
        if set(self.editable_fields) == set(LEGACY_EDITABLE_FIELDS):
            self.version = "v1"
        elif set(self.editable_fields) >= set(DEFAULT_EDITABLE_FIELDS):
            self.version = "v2"

        min_length_fields = [
            "russian_word_reaction",
            "admin_decision_attitude",
            "new_rule_reaction",
            "useful_skills_detailed",
            "server_experience_negative",
            "long_project_experience",
            "community_projects_readiness",
            "healthy_community_definition",
            "ideal_server_description",
        ]

        for field in min_length_fields:
            value = getattr(self, field, None)
            if value and isinstance(value, str):
                char_count = len(value.strip())
                if char_count < 30:
                    raise ValueError(
                        f"{field} must contain at least 30 characters (current: {char_count})"
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
