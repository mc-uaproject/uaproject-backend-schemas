from typing import Any, Dict, Optional

from uaproject_backend_schemas.base import (
    BothPayloadBaseModel,
    PayloadBaseModel,
    PayloadBoth,
    TimestampsMixin,
    UsersIDMixin,
)
from uaproject_backend_schemas.schemas import SerializableDecimal

from .schemas import TransactionType

__all__ = [
    "TransactionBasePayload",
    "TransactionCreatedPayload",
    "TransactionTypePayload",
    "TransactionAmountPayload",
    "TransactionCreatedPayloadFull",
    "TransactionTypePayloadFull",
    "TransactionAmountPayloadFull",
    "TransactionFullMixins",
]


class TransactionBasePayload(UsersIDMixin):
    """Base payload for transactions"""

    amount: SerializableDecimal
    type: TransactionType
    description: Optional[str] = None


class TransactionCreatedPayload(TransactionBasePayload):
    """Payload for transaction creation"""

    id: int
    user_id: int
    recipient_id: Optional[int] = None
    service_id: Optional[int] = None
    transaction_metadata: Optional[Dict[str, Any]] = None


class TransactionTypePayload(TransactionBasePayload):
    """Payload for transaction type updates"""

    id: int
    user_id: int
    amount: SerializableDecimal
    type: TransactionType
    description: Optional[str] = None


class TransactionAmountPayload(TransactionBasePayload):
    """Payload for transaction amount updates"""

    id: int
    user_id: int
    amount: SerializableDecimal
    type: TransactionType
    description: Optional[str] = None


class TransactionCreatedPayloadFull(PayloadBaseModel):
    """Full transaction created payload wrapper"""

    payload: TransactionCreatedPayload


class TransactionTypePayloadFull(BothPayloadBaseModel):
    """Full transaction type payload wrapper"""

    payload: dict[PayloadBoth, TransactionTypePayload]


class TransactionAmountPayloadFull(BothPayloadBaseModel):
    """Full transaction amount payload wrapper"""

    payload: dict[PayloadBoth, TransactionAmountPayload]


class TransactionFullMixins(TransactionCreatedPayload, TimestampsMixin):
    """Mixin combining transaction payload with timestamp"""

    pass
