from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.base import BaseResponseModel
from uaproject_backend_schemas.schemas import UserDefaultSort

__all__ = [
    "PunishmentType",
    "PunishmentStatus",
    "PunishmentSort",
    "PunishmentBase",
    "PunishmentCreate",
    "PunishmentUpdate",
    "PunishmentResponse",
    "PunishmentFilterParams",
]


class PunishmentType(StrEnum):
    WARN = "warn"
    MUTE = "mute"
    BAN = "ban"
    KICK = "kick"
    RESTRICTION = "restriction"


class PunishmentStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class PunishmentSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    TYPE = "type"
    STATUS = "status"
    USER_ID = UserDefaultSort.USER_ID
    EXPIRES_AT = "expires_at"


class PunishmentBase(BaseResponseModel):
    user_id: int
    admin_id: Optional[int] = None
    type: PunishmentType
    status: PunishmentStatus = PunishmentStatus.ACTIVE
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    config_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class PunishmentCreate(PunishmentBase):
    pass


class PunishmentUpdate(BaseModel):
    status: Optional[PunishmentStatus] = None
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class PunishmentResponse(PunishmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PunishmentFilterParams(BaseModel):
    user_id: Optional[int] = None
    admin_id: Optional[int] = None
    type: Optional[PunishmentType] = None
    status: Optional[PunishmentStatus] = None
    min_created_at: Optional[datetime] = None
    max_created_at: Optional[datetime] = None
    min_expires_at: Optional[datetime] = None
    max_expires_at: Optional[datetime] = None
    config_id: Optional[int] = None


class PunishmentConfigBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    warn_threshold: int = 3
    warn_decay_days: int = 30
    config_data: Dict[str, Any] = {}


class PunishmentConfigCreate(PunishmentConfigBase):
    pass


class PunishmentConfigUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    warn_threshold: Optional[int] = None
    warn_decay_days: Optional[int] = None
    config_data: Optional[Dict[str, Any]] = None


class PunishmentConfigResponse(PunishmentConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
