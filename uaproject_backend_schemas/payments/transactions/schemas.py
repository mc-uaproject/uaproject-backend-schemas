from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, Optional

from pydantic import BaseModel, field_validator

from uaproject_backend_schemas.base import BaseResponseModel, TimestampsMixin
from uaproject_backend_schemas.payments.services.schemas import ServiceResponse
from uaproject_backend_schemas.schemas import SerializableDecimal, UserDefaultSort

__all__ = [
    "TransactionType",
    "TransactionBase",
    "TransactionFilterParams",
    "TransactionSort",
    "DepositTransaction",
    "TransferTransaction",
    "PurchaseTransaction",
    "WithdrawalTransaction",
    "SystemDepositTransaction",
    "RefundTransaction",
    "AdjustmentTransaction",
    "DonationTransaction",
    "TransactionUpdate",
    "TransactionResponse",
]


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PURCHASE = "purchase"
    DONATION = "donation"
    SYSTEM = "system"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"


class TransactionBase(BaseResponseModel):
    amount: Optional[SerializableDecimal] = None
    recipient_id: Optional[int] = None
    type: TransactionType
    description: Optional[str] = None
    transaction_metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[int] = None
    service_id: Optional[int] = None


class TransactionFilterParams(BaseModel):
    user_id: Optional[int] = None
    recipient_id: Optional[int] = None
    service_id: Optional[int] = None
    type: Optional[TransactionType] = None
    min_amount: Optional[SerializableDecimal] = None
    max_amount: Optional[SerializableDecimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TransactionSort(StrEnum):
    ID = UserDefaultSort.ID
    CREATED_AT = UserDefaultSort.CREATED_AT
    UPDATED_AT = UserDefaultSort.UPDATED_AT
    AMOUNT = "amount"
    TYPE = "type"


class DepositTransaction(TransactionBase):
    type: TransactionType = TransactionType.DEPOSIT

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v != TransactionType.DEPOSIT:
            raise ValueError("Transaction type must be DEPOSIT")
        return v


class TransferTransaction(TransactionBase):
    type: TransactionType = TransactionType.TRANSFER

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v != TransactionType.TRANSFER:
            raise ValueError("Transaction type must be TRANSFER")
        return v


class PurchaseTransaction(TransactionBase):
    type: TransactionType = TransactionType.PURCHASE
    service_id: int
    amount: Optional[SerializableDecimal] = None
    recipient_id: Optional[int] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v != TransactionType.PURCHASE:
            raise ValueError("Transaction type must be PURCHASE")
        return v


class WithdrawalTransaction(TransactionBase):
    type: TransactionType = TransactionType.WITHDRAWAL

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v != TransactionType.WITHDRAWAL:
            raise ValueError("Transaction type must be WITHDRAWAL")
        return v


class SystemDepositTransaction(TransactionBase):
    type: TransactionType = TransactionType.SYSTEM
    transaction_metadata: Optional[Dict[str, Any]] = None


class RefundTransaction(TransactionBase):
    type: TransactionType = TransactionType.REFUND
    original_transaction_id: int
    reason: str


class AdjustmentTransaction(TransactionBase):
    type: TransactionType = TransactionType.ADJUSTMENT
    reason: str


class DonationTransaction(TransactionBase):
    type: TransactionType = TransactionType.DONATION
    description: str
    donor_name: Optional[str] = None
    donor_email: Optional[str] = None
    source: Optional[str] = None
    original_currency: Optional[str] = None
    original_amount: Optional[SerializableDecimal] = None


class TransactionUpdate(BaseModel):
    amount: Optional[SerializableDecimal] = None
    type: Optional[TransactionType] = None
    description: Optional[str] = None
    service_id: Optional[int] = None
    transaction_metadata: Optional[Dict[str, Any]] = None


class TransactionResponse(TransactionBase, TimestampsMixin):
    id: int
    recipient_id: int
    service_id: Optional[int] = None
    service: Optional[ServiceResponse] = None

    class Config:
        from_attributes = True
