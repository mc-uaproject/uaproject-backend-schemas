from datetime import datetime
from enum import StrEnum
from typing import Dict, Optional

from pydantic import BaseModel, HttpUrl

from uaproject_backend_schemas.schemas import UserDefaultSort

__all__ = [
    "WebhookSort",
    "WebhookStatus",
    "WebhookBase",
    "WebhookCreate",
    "WebhookUpdate",
    "WebhookResponse",
    "WebhookFilterParams",
    "WebhookStage",
]


class WebhookSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    STATUS = "status"
    ENDPOINT = "endpoint"


class WebhookStatus(StrEnum):
    ACTIVE = "active"
    UNRESPONSIVE = "unresponsive"
    PROCESSING = "processing"
    ERROR = "error"


class WebhookBase(BaseModel):
    endpoint: HttpUrl
    scopes: Dict[str, bool]
    authorization: Optional[str] = None


class WebhookCreate(WebhookBase):
    status: WebhookStatus = WebhookStatus.ACTIVE


class WebhookUpdate(WebhookBase):
    status: Optional[WebhookStatus] = None


class WebhookStage(StrEnum):
    AFTER = "after"
    BEFORE = "before"
    BOTH = "both"


class WebhookResponse(WebhookBase):
    id: int
    status: WebhookStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WebhookFilterParams(BaseModel):
    user_id: Optional[int] = None
    status: Optional[WebhookStatus] = None
    min_created_at: Optional[datetime] = None
    max_created_at: Optional[datetime] = None
