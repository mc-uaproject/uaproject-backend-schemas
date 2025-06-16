from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlmodel import JSON, Column

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType


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
    status: ServerAccessStatus = AwesomeField(default=ServerAccessStatus.PENDING, index=True)
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
