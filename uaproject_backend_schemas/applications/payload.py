from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.applications.schemas import ApplicationStatus
from uaproject_backend_schemas.base import (
    BothPayloadBaseModel,
    PayloadBaseModel,
    PayloadBoth,
    TimestampsMixin,
    UsersIDMixin,
)

__all__ = [
    "ApplicationStatusPayload",
    "ApplicationFormPayload",
    "ApplicationFormPayloadFull",
    "ApplicationFullMixins",
    "ApplicationFieldEditableResponse",
    "ApplicationStatusPayloadFull",
]


class ApplicationStatusPayload(UsersIDMixin):
    """Payload for application status"""

    status: ApplicationStatus


class ApplicationFormPayload(ApplicationStatusPayload):
    """Detailed form payload"""

    birth_date: Optional[datetime] = None
    launcher: Optional[str] = None
    server_source: Optional[str] = None
    private_server_experience: Optional[str] = None
    useful_skills: Optional[str] = None
    conflict_reaction: Optional[str] = None
    quiz_answer: Optional[str] = None


class ApplicationFormPayloadFull(PayloadBaseModel):
    """Full form payload wrapper"""

    payload: ApplicationFormPayload


class ApplicationStatusPayloadFull(BothPayloadBaseModel):
    """Full status payload wrapper"""

    payload: dict[PayloadBoth, ApplicationStatusPayload]


class ApplicationFullMixins(ApplicationFormPayload, TimestampsMixin):
    """Mixin combining form payload with timestamp"""

    pass


class ApplicationFieldEditableResponse(BaseModel):
    """Response for checking if a specific field is editable"""

    editable: bool
