from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, List, Optional

from pydantic import model_validator
from sqlmodel import ARRAY, BigInteger, Column, Enum, Field, ForeignKey, Relationship, String

from uaproject_backend_schemas.applications.payload import (
    ApplicationFormPayload,
    ApplicationStatusPayload,
)
from uaproject_backend_schemas.applications.schemas import ApplicationStatus
from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.webhooks.mixins import (
    WebhookBaseMixin,
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
)
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User


__all__ = ["Application"]


class Application(
    WebhookBaseMixin,
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
    TimestampsMixin,
    IDMixin,
    Base,
    table=True,
):
    __tablename__ = "applications"
    __scope_prefix__ = "application"

    DEFAULT_EDITABLE_FIELDS: ClassVar[List[str]] = [
        "birth_date",
        "launcher",
        "server_source",
        "private_server_experience",
        "useful_skills",
        "conflict_reaction",
        "quiz_answer",
    ]

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False, unique=True))
    user: Optional["User"] = Relationship(
        back_populates="application", sa_relationship_kwargs={"uselist": False}
    )

    status: ApplicationStatus = Field(
        sa_column=Column(
            Enum(ApplicationStatus, native_enum=False),
            default=ApplicationStatus.NOT_SENT.value,
            server_default=ApplicationStatus.NOT_SENT.value,
        )
    )

    birth_date: datetime = Field(nullable=True)
    launcher: str = Field(max_length=32, nullable=True)
    server_source: str = Field(max_length=512, nullable=True)
    private_server_experience: str = Field(max_length=1024, nullable=True)
    useful_skills: str = Field(max_length=1024, nullable=True)
    conflict_reaction: str = Field(max_length=1024, nullable=True)
    quiz_answer: str = Field(max_length=1024, nullable=True)

    editable_fields: List[str] = Field(
        sa_column=Column(
            ARRAY(String),
            nullable=False,
            default=DEFAULT_EDITABLE_FIELDS,
            server_default="{}",
        )
    )

    @model_validator(mode="before")
    def truncate_fields(self) -> "Application":
        max_lengths = {
            "launcher": 32,
            "server_source": 512,
            "private_server_experience": 1024,
            "useful_skills": 1024,
            "conflict_reaction": 1024,
            "quiz_answer": 1024,
        }

        for field, max_length in max_lengths.items():
            value = getattr(self, field)
            if value and len(value) > max_length:
                setattr(self, field, value[:max_length])

        return self

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "status",
            trigger_fields={"status"},
            fields=ApplicationStatusPayload.model_construct(),
            stage=WebhookStage.BOTH,
        )
        cls.register_scope(
            "editable_fields",
            trigger_fields={"editable_fields"},
            fields={"id", "user_id", "editable_fields"},
            stage=WebhookStage.AFTER,
        )
        form_fields = set(cls.__table__.columns.keys()) - {"status"}
        cls.register_scope(
            "form",
            trigger_fields=form_fields,
            fields=ApplicationFormPayload.model_construct(),
            stage=WebhookStage.AFTER,
        )
        cls.register_scope(
            "full", trigger_fields=set(cls.__table__.columns.keys()), stage=WebhookStage.AFTER
        )

    def is_field_editable(self, field_name: str) -> bool:
        return field_name in self.editable_fields
