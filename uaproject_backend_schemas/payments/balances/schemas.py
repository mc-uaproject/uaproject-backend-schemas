from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.schemas import SerializableDecimal, UserDefaultSort

__all__ = ["BalanceUpdate", "BalanceResponse", "BalanceFilterParams", "BalanceSort"]


class BalanceUpdate(BaseModel):
    amount: Optional[SerializableDecimal] = None


class BalanceResponse(BaseModel):
    id: int
    user_id: int
    identifier: UUID
    amount: SerializableDecimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {UUID: str}  # noqa: RUF012


class BalanceFilterParams(BaseModel):
    user_id: Optional[int] = None
    min_amount: Optional[SerializableDecimal] = None
    max_amount: Optional[SerializableDecimal] = None


class BalanceSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    AMOUNT = "amount"
