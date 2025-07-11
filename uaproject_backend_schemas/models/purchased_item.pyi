# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.purchased_item import PurchasedItemStatus
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.transaction import Transaction
from uaproject_backend_schemas.models.user import User

class PurchasedItem(AwesomeModel):
    """Base purchaseditem model."""

    created_at: datetime
    expires_at: Optional[datetime]
    id: int
    purchase_metadata: Optional[dict[str, Any]]
    quantity: int
    servers: list[str]
    service: Optional[Service]
    service_id: int
    status: PurchasedItemStatus
    transaction: Optional[Transaction]
    transaction_id: int
    updated_at: datetime
    user: Optional[User]
    user_id: int
    schemas: PurchasedItemSchemas
    filter: type[PurchasedItemFilter]
    sort: type[PurchasedItemSort]

class PurchasedItemSchemas:
    """Schemas for the PurchasedItem model."""

    create: PurchasedItemSchemaCreate
    redis: PurchasedItemSchemaRedis
    response: PurchasedItemSchemaResponse
    update: PurchasedItemSchemaUpdate

class PurchasedItemSchemaCreate(AwesomeBaseModel):
    """create schema for PurchasedItem model"""

    user_id: Optional[int]
    quantity: Optional[int]
    purchase_metadata: Optional[dict[str, Any]]
    servers: Optional[list[str]]
    service_id: Optional[int]
    transaction_id: Optional[int]
    status: Optional[PurchasedItemStatus]
    expires_at: Optional[datetime]

class PurchasedItemSchemaRedis(AwesomeBaseModel):
    """redis schema for PurchasedItem model"""

    user_id: Optional[int]
    quantity: Optional[int]
    purchase_metadata: Optional[dict[str, Any]]
    service: Optional[Service]
    updated_at: Optional[datetime]
    servers: Optional[list[str]]
    user: Optional[User]
    service_id: Optional[int]
    transaction: Optional[Transaction]
    transaction_id: Optional[int]
    id: Optional[int]
    status: Optional[PurchasedItemStatus]
    expires_at: Optional[datetime]
    created_at: datetime

class PurchasedItemSchemaResponse(AwesomeBaseModel):
    """response schema for PurchasedItem model"""

    user_id: Optional[int]
    quantity: Optional[int]
    purchase_metadata: Optional[dict[str, Any]]
    updated_at: Optional[datetime]
    servers: Optional[list[str]]
    service_id: Optional[int]
    transaction_id: Optional[int]
    id: Optional[int]
    status: Optional[PurchasedItemStatus]
    expires_at: Optional[datetime]
    created_at: datetime

class PurchasedItemSchemaUpdate(AwesomeBaseModel):
    """update schema for PurchasedItem model"""

    user_id: Optional[int]
    quantity: Optional[int]
    purchase_metadata: Optional[dict[str, Any]]
    servers: Optional[list[str]]
    service_id: Optional[int]
    transaction_id: Optional[int]
    status: Optional[PurchasedItemStatus]
    expires_at: Optional[datetime]

class PurchasedItemFilter(BaseModel):
    """Pydantic-class for filtering the PurchasedItem model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    service_id: Optional[int] = None
    min_service_id: Optional[int] = None
    max_service_id: Optional[int] = None
    transaction_id: Optional[int] = None
    min_transaction_id: Optional[int] = None
    max_transaction_id: Optional[int] = None
    status: Optional[PurchasedItemStatus] = None
    quantity: Optional[int] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    expires_at: Optional[datetime] = None
    min_expires_at: Optional[datetime] = None
    max_expires_at: Optional[datetime] = None
    service_name: Optional[str] = None

class PurchasedItemSort(StrEnum):
    """Enum for sorting the PurchasedItem model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
