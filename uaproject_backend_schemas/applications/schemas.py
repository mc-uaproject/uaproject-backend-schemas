from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from uaproject_backend_schemas.base import BaseResponseModel
from uaproject_backend_schemas.schemas import UserDefaultSort

__all__ = [
    "ApplicationSort",
    "ApplicationStatus",
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationFilterParams",
    "EditableFieldsResponse",
]


class ApplicationSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    STATUS = "status"
    USER_ID = "user_id"


class ApplicationStatus(StrEnum):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    REVIEW = "review"
    EDITING = "editing"
    NOT_SENT = "not_sent"


class ApplicationBase(BaseResponseModel):
    birth_date: Optional[datetime] = None
    launcher: Optional[str] = Field(None, max_length=32)
    server_source: Optional[str] = Field(None, max_length=512)
    private_server_experience: Optional[str] = Field(None, max_length=1024)
    useful_skills: Optional[str] = Field(None, max_length=1024)
    conflict_reaction: Optional[str] = Field(None, max_length=1024)
    quiz_answer: Optional[str] = Field(None, max_length=1024)

    @field_validator(
        "launcher",
        "server_source",
        "private_server_experience",
        "useful_skills",
        "conflict_reaction",
        "quiz_answer",
        mode="before",
    )
    @classmethod
    def truncate_field(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if isinstance(v, str) and info.data.get("max_length"):
            return v[: info.data["max_length"]]
        return v


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    status: Optional[ApplicationStatus] = None
    editable_fields: Optional[List[str]] = None


class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    status: ApplicationStatus
    editable_fields: List[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationFilterParams(BaseModel):
    user_id: Optional[int] = None
    status: Optional[ApplicationStatus] = None
    min_created_at: Optional[datetime] = None
    max_created_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None


class EditableFieldsResponse(BaseModel):
    """Response for retrieving editable fields"""

    editable_fields: List[str]
