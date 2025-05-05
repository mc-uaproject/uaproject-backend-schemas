from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class ServiceCategory(StrEnum):
    DONATION = "donation"
    SERVICE = "service"


class ServiceType(StrEnum):
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"


class ServicePoint(BaseModel):
    text: str
    tooltip: Optional[str] = None


class ServiceDiscount(BaseModel):
    user_id: Optional[int] = None
    discount_percent: float
    start_date: datetime
    end_date: Optional[datetime] = None
    reason: Optional[str] = None
