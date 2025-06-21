from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import model_validator
from sqlalchemy import BigInteger, ForeignKey
from sqlmodel import JSON, Column

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType

# Evervault section fields
EVERVAULT_REQUIRED_FIELDS = [
    "long_project_experience",
    "community_projects_readiness",
    "healthy_community_definition",
    "ideal_server_description",
]


class ApplicationSection(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    """Server-specific section of an application."""

    __tablename__ = "application_sections"

    application_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("applications.id"), nullable=False, index=True)
    )
    server_type: ServerType = AwesomeField(index=True)
    section_data: dict = AwesomeField(
        sa_column=Column(JSON, nullable=False, default={}),
        default_factory=dict,
        description="JSON data for server-specific fields",
    )

    # Review status for this server
    status: ServerAccessStatus = AwesomeField(default=ServerAccessStatus.NOT_APPLIED, index=True)
    reviewed_by: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True), default=None
    )
    reviewed_at: Optional[datetime] = AwesomeField(default=None)
    rejection_reason: Optional[str] = AwesomeField(default=None, max_length=1000)
    is_required: bool = AwesomeField(
        default=True, description="Whether this section is required for server access"
    )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = [
                "id",
                "created_at",
                "updated_at",
                "reviewed_by",
                "reviewed_at",
                "status",
            ]
            optional = True

        class Update(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "application_id", "server_type"]
            optional = True

        class AdminUpdate(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "application_id"]
            optional = True

        class Response(SchemaDefinition):
            pass

        class ResponseDetailed(SchemaDefinition):
            pass

    class Scopes(AwesomeModel.Scopes):
        class CreateOwn(ScopeDefinition):
            description = "Create application sections for own applications"
            permissions = [".create.self"]

        class UpdateOwn(ScopeDefinition):
            description = "Update own application sections"
            permissions = [".update.self"]

        class AdminReview(ScopeDefinition):
            description = "Review and manage application sections"
            permissions = [".update.admin", ".read.admin"]

    @model_validator(mode="after")
    def validate_section_data(self):
        """Validate section data based on server type."""
        if self.server_type == ServerType.EVERVAULT and self.section_data:
            # Validate Evervault fields have minimum character count
            for field_name in EVERVAULT_REQUIRED_FIELDS:
                field_value = self.section_data.get(field_name)
                if field_value and isinstance(field_value, str):
                    char_count = len(field_value.strip())
                    if char_count < 30:
                        raise ValueError(
                            f"Evervault field '{field_name}' must contain at least 30 characters (current: {char_count})"
                        )

        return self
