from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.base import BaseResponseModel
from uaproject_backend_schemas.schemas import SerializableDecimal, UserDefaultSort

__all__ = [
    "ServiceSort",
    "ServiceBase",
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceResponse",
    "ServiceFilterParams",
]


class ServiceSort(StrEnum):
    CREATED_AT = UserDefaultSort.CREATED_AT
    NAME = "name"
    PRICE = "price"


class ServiceBase(BaseResponseModel):
    name: str
    description: Optional[str] = None
    price: SerializableDecimal
    currency: str = "UAH"
    is_active: bool = True
    category: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[SerializableDecimal] = None
    currency: Optional[str] = None
    is_active: Optional[bool] = None
    category: Optional[str] = None


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True


class ServiceFilterParams(BaseModel):
    is_active: Optional[bool] = None
    category: Optional[str] = None
    name: Optional[str] = None
