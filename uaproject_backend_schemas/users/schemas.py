from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from uaproject_backend_schemas.base import BaseResponseModel
from uaproject_backend_schemas.schemas import UserDefaultSort

__all__ = [
    "TokenResponse",
    "UserTokenResponse",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserFilterParams",
    "UserSort",
    "SearchMode",
]


class SearchMode(StrEnum):
    SIMILAR = "similar"
    ANY = "any"


class TokenResponse(BaseModel):
    token: UUID


class UserTokenResponse(BaseResponseModel):
    token: UUID
    user_id: int
    created_at: datetime


class UserCreate(BaseResponseModel):
    minecraft_nickname: Optional[str] = None
    discord_id: Optional[int] = None
    is_superuser: Optional[bool] = False


class UserUpdate(BaseModel):
    minecraft_nickname: Optional[str] = None
    discord_id: Optional[int] = None
    is_superuser: Optional[bool] = None

    @model_validator(mode="before")
    def validate_minecraft_nickname(cls, values):
        nickname = values.get("minecraft_nickname")
        if nickname is not None:
            if not 3 <= len(nickname) <= 16:
                raise ValueError("Minecraft nickname must be between 3 and 16 characters.")
            if not nickname.isalnum() and "_" not in nickname:
                raise ValueError(
                    "Minecraft nickname can only contain letters, numbers, and underscores."
                )
        return values


class UserResponse(BaseResponseModel):
    id: int
    discord_id: Optional[int] = None
    minecraft_nickname: Optional[str] = None
    is_superuser: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class UserFilterParams(BaseModel):
    user_id: Optional[int] = None
    discord_id: Optional[int] = None
    minecraft_nickname: Optional[str] = None
    is_superuser: Optional[bool] = None
    role_name: Optional[str] = None


class UserSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    MINECRAFT_NICKNAME = "minecraft_nickname"
    DISCORD_ID = "discord_id"
    ROLE_WEIGHT = "role_weight"
