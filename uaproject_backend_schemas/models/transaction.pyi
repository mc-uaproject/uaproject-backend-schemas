# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.purchased_item import PurchasedItem
from uaproject_backend_schemas.models.schemas.transaction import TransactionType
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.user import User

class Transaction(AwesomeModel):
    """Base transaction model."""

    amount: Decimal
    created_at: datetime
    description: Optional[str]
    id: int
    purchased_item: Optional[PurchasedItem]
    recipient: Optional[User]
    recipient_id: int
    service: Optional[Service]
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    type: TransactionType
    updated_at: datetime
    user: Optional[User]
    user_id: int
    schemas: TransactionSchemas
    filter: type[TransactionFilter]
    sort: type[TransactionSort]

class TransactionSchemas:
    """Schemas for the Transaction model."""

    create: TransactionSchemaCreate
    redis: TransactionSchemaRedis
    response: TransactionSchemaResponse
    update: TransactionSchemaUpdate

class TransactionSchemaCreate(AwesomeBaseModel):
    """create schema for Transaction model"""

    type: Optional[TransactionType]
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    description: Optional[str]
    amount: Optional[Decimal]
    recipient_id: Optional[int]
    user_id: Optional[int]

class TransactionSchemaRedis(AwesomeBaseModel):
    """redis schema for Transaction model"""

    type: Optional[TransactionType]
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    purchased_item: Optional[PurchasedItem]
    id: Optional[int]
    description: Optional[str]
    amount: Optional[Decimal]
    user: Optional[User]
    updated_at: Optional[datetime]
    recipient_id: Optional[int]
    recipient: Optional[User]
    user_id: Optional[int]
    service: Optional[Service]
    created_at: datetime

class TransactionSchemaResponse(AwesomeBaseModel):
    """response schema for Transaction model"""

    type: TransactionType
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    id: Optional[int]
    description: Optional[str]
    amount: Decimal
    updated_at: Optional[datetime]
    recipient_id: int
    user_id: int
    created_at: datetime

class TransactionSchemaUpdate(AwesomeBaseModel):
    """update schema for Transaction model"""

    type: Optional[TransactionType]
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    description: Optional[str]
    amount: Optional[Decimal]
    recipient_id: Optional[int]
    user_id: Optional[int]

class TransactionFilter(BaseModel):
    """Pydantic-class for filtering the Transaction model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    description: Optional[str] = None
    recipient_id: Optional[int] = None
    min_recipient_id: Optional[int] = None
    max_recipient_id: Optional[int] = None
    service_id: Optional[int] = None
    min_service_id: Optional[int] = None
    max_service_id: Optional[int] = None
    service_name: Optional[str] = None
    purchased_item_id: Optional[int] = None

class TransactionSort(StrEnum):
    """Enum for sorting the Transaction model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
