from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.base import BaseResponseModel

__all__ = ["RoleSort", "RoleCreate", "RoleUpdate", "RoleFilterParams", "RoleResponse"]


class RoleSort(StrEnum):
    NAME = "name"
    WEIGHT = "weight"
    CREATED_AT = "created_at"


class RoleCreate(BaseModel):
    name: str
    display_name: Optional[str] = None
    permissions: List[str]
    weight: int = 0


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    permissions: Optional[List[str]] = None
    weight: Optional[int] = None


class RoleFilterParams(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    weight: Optional[int] = None
    display_name: Optional[str] = None


class RoleResponse(BaseResponseModel):
    id: int
    name: str
    display_name: Optional[str] = None
    permissions: List[str]
    weight: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
