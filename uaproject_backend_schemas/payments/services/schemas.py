from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from uaproject_backend_schemas.base import BaseResponseModel
from uaproject_backend_schemas.schemas import SerializableDecimal, UserDefaultSort

__all__ = [
    "ServiceSort",
    "ServiceBase",
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceResponse",
    "ServiceFilterParams",
    "ServicePoint",
    "ServicePoints",
    "ServiceDiscount",
    "ServiceMetadata",
]


class ServiceSort(StrEnum):
    CREATED_AT = UserDefaultSort.CREATED_AT
    NAME = "name"
    PRICE = "price"


class ServiceCategory(StrEnum):
    DONATION = "donation"
    SERVICE = "service"


class ServiceType(StrEnum):
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"


class ServicePoint(BaseModel):
    text: str
    tooltip: Optional[str] = None


class ServicePoints(BaseModel):
    title: str
    identifier: str
    discount: Optional[float] = 0
    sub_title: Optional[str] = None
    img: Optional[str] = None
    price: float
    price_sub_title: Optional[str] = None
    points: List[ServicePoint]


class ServiceDiscount(BaseModel):
    user_id: Optional[int] = None
    discount_percent: float
    start_date: datetime
    end_date: Optional[datetime] = None
    reason: Optional[str] = None


class ServiceMetadata(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class ServiceBase(BaseResponseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    points: Optional[List[ServicePoints]] = None
    image: Optional[str] = None
    price: SerializableDecimal
    is_active: bool = True
    category: Optional[str] = None
    type: ServiceType
    duration_months: Optional[int] = None
    is_upgradable: Optional[bool] = False
    upgrade_from: Optional[str] = None
    upgrade_to: Optional[str] = None
    service_metadata: Optional[ServiceMetadata] = None
    discounts: Optional[List[ServiceDiscount]] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    points: Optional[List[ServicePoints]] = None
    image: Optional[str] = None
    price: Optional[SerializableDecimal] = None
    is_active: Optional[bool] = None
    category: Optional[str] = None
    type: Optional[ServiceType] = None
    duration_months: Optional[int] = None
    is_upgradable: Optional[bool] = None
    upgrade_from: Optional[str] = None
    upgrade_to: Optional[str] = None
    service_metadata: Optional[ServiceMetadata] = None
    discounts: Optional[List[ServiceDiscount]] = None


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
    type: Optional[ServiceType] = None
    is_upgradable: Optional[bool] = None
