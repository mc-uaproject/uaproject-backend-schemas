from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import model_validator
from sqlmodel import ARRAY, BigInteger, Column, Enum, ForeignKey, Relationship, String

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition
from uaproject_backend_schemas.models.schemas.application import ApplicationStatus

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User

DEFAULT_EDITABLE_FIELDS: List[str] = [
    "birth_date",
    "launcher",
    "server_source",
    "private_server_experience",
    "useful_skills",
    "conflict_reaction",
    "quiz_answer",
]


class Application(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    __tablename__ = "applications"
    __scope_prefix__ = "application"
    model_config = {"arbitrary_types_allowed": True}

    user_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False, unique=True)
    )
    status: ApplicationStatus = AwesomeField(
        sa_column=Column(
            Enum(ApplicationStatus, native_enum=False),
            default=ApplicationStatus.NOT_SENT.value,
            server_default=ApplicationStatus.NOT_SENT.value,
        )
    )

    birth_date: Optional[datetime] = AwesomeField(nullable=True)
    launcher: Optional[str] = AwesomeField(max_length=32, nullable=True)
    server_source: Optional[str] = AwesomeField(max_length=512, nullable=True)
    private_server_experience: Optional[str] = AwesomeField(max_length=1024, nullable=True)
    useful_skills: Optional[str] = AwesomeField(max_length=1024, nullable=True)
    conflict_reaction: Optional[str] = AwesomeField(max_length=1024, nullable=True)
    quiz_answer: Optional[str] = AwesomeField(max_length=1024, nullable=True)

    editable_fields: List[str] = AwesomeField(
        sa_column=Column(
            ARRAY(String),
            nullable=False,
            default=DEFAULT_EDITABLE_FIELDS,
            server_default="{}",
        )
    )

    user: Optional["User"] = Relationship(
        back_populates="application", sa_relationship_kwargs={"uselist": False}
    )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "user_id", "status"]
            optional = True
            permissions = [".write.self"]

        class Update(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "user_id", "status"]
            optional = True
            permissions = [".write.self"]

        class UpdateStatus(SchemaDefinition):
            fields = ["status"]
            permissions = [".admin"]

        class Response(SchemaDefinition):
            permissions = [".read.other"]

        class ResponseSelf(SchemaDefinition):
            permissions = [".read.self"]

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
        for field in [
            "private_server_experience",
            "useful_skills",
            "conflict_reaction",
            "quiz_answer",
        ]:
            cls._validate_text_length(field, values.get(field))

        if editable_fields := values.get("editable_fields"):
            if not isinstance(editable_fields, list):
                raise ValueError("Editable fields must be a list")
            if not all(field in cls.DEFAULT_EDITABLE_FIELDS for field in editable_fields):
                raise ValueError("Invalid editable fields")

        return values
