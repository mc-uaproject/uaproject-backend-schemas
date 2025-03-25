from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
from pydantic import Field as PydanticField

from uaproject_backend_schemas.schemas import SerializableDecimal, UserDefaultSort

__all__ = ["DonationSort", "DonationFilterParams", "DonationBase", "DonationCreate", "DonationUpdate", "DonationResponse"]


class DonationSort(StrEnum):
    ID = UserDefaultSort.ID
    AMOUNT = "amount"
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT


class DonationFilterParams(BaseModel):
    user_id: Optional[int] = None
    min_amount: Optional[SerializableDecimal] = None
    max_amount: Optional[SerializableDecimal] = None
    currency: Optional[str] = PydanticField(None, min_length=3, max_length=3)
    source: Optional[str] = PydanticField(None, max_length=50)

    @field_validator("min_amount", "max_amount")
    def validate_amount(cls, v):
        if v is not None and v < 0:
            raise ValueError("Amount cannot be negative")
        return v

    @field_validator("max_amount")
    def validate_max_amount(cls, v, values):
        if v is not None and "min_amount" in values and values["min_amount"] is not None:
            if v < values["min_amount"]:
                raise ValueError("max_amount cannot be less than min_amount")
        return v


class DonationBase(BaseModel):
    amount: SerializableDecimal = PydanticField(..., gt=0)
    currency: str = PydanticField(..., min_length=3, max_length=3)
    donor_name: str = PydanticField(..., max_length=255)
    donor_email: EmailStr
    message: str = PydanticField(..., max_length=1000)
    source: str = PydanticField(..., max_length=50)


class DonationCreate(DonationBase):
    user_id: int
    balance_id: int
    donatello_transaction_id: str = PydanticField(..., max_length=255)


class DonationUpdate(BaseModel):
    amount: Optional[SerializableDecimal] = None
    currency: Optional[str] = None
    donor_name: Optional[str] = None
    donor_email: Optional[EmailStr] = None
    message: Optional[str] = None
    source: Optional[str] = None


class DonationResponse(DonationBase):
    id: int
    user_id: int
    balance_id: int
    donatello_transaction_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
