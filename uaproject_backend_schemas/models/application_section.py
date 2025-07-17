from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import JSON, BigInteger, Column, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.models.schemas.server import ServerAccessStatus, ServerType

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.application import Application


class ApplicationSection(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    """Server-specific section of an application."""

    __tablename__ = "application_sections"
    __scope_prefix__ = "application_section"

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
    application: "Application" = Relationship(
        back_populates="sections",
        sa_relationship_kwargs={
            "foreign_keys": "[ApplicationSection.application_id]",
        },
    )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = [
                "id",
                "created_at",
                "updated_at",
                "reviewed_by",
                "reviewed_at",
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
