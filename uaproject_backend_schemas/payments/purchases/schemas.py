from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field

from uaproject_backend_schemas.schemas import UserDefaultSort

__all__ = ["PurchasedItemStatus", "PurchasedItemSort", "PurchasedItemBase", "PurchasedItemCreate", "PurchasedItemUpdate", "PurchasedItemResponse", "PurchasedItemFilterParams"]

class PurchasedItemStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class PurchasedItemSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    STATUS = "status"
    SERVICE_ID = "service_id"


class PurchasedItemBase(BaseModel):
    service_id: int
    status: PurchasedItemStatus = PurchasedItemStatus.ACTIVE
    quantity: int = Field(default=1, ge=1)
    time_spent: int = 0
    transaction_id: int


class PurchasedItemCreate(PurchasedItemBase):
    pass


class PurchasedItemUpdate(BaseModel):
    status: Optional[PurchasedItemStatus] = None
    quantity: Optional[int] = None
    time_spent: Optional[int] = None


class PurchasedItemResponse(PurchasedItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PurchasedItemFilterParams(BaseModel):
    status: Optional[PurchasedItemStatus] = None
    service_id: Optional[int] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_time_spent: Optional[int] = None
    max_time_spent: Optional[int] = None
