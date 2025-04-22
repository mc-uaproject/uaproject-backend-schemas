from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from uaproject_backend_schemas.base import BaseResponseModel
from uaproject_backend_schemas.schemas import SerializableDecimal, UserDefaultSort

__all__ = ["BalanceUpdate", "BalanceResponse", "BalanceFilterParams", "BalanceSort"]


class BalanceUpdate(BaseModel):
    amount: Optional[SerializableDecimal] = None


class BalanceResponse(BaseResponseModel):
    id: int
    user_id: int
    identifier: UUID
    amount: SerializableDecimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('identifier')
    def serialize_identifier(self, identifier: UUID, _info):
        return str(identifier)


class BalanceFilterParams(BaseModel):
    user_id: Optional[int] = None
    identifier: Optional[UUID] = None
    min_amount: Optional[SerializableDecimal] = None
    max_amount: Optional[SerializableDecimal] = None


class BalanceSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    AMOUNT = "amount"
