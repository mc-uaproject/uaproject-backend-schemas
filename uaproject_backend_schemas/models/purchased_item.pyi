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

    expires_at: Optional[datetime]
    id: int
    purchase_metadata: Optional[dict[str, Any]]
    quantity: int
    service: Optional[Service]
    service_id: int
    status: PurchasedItemStatus
    transaction: Optional[Transaction]
    transaction_id: int
    updated_at: datetime
    user: Optional[User]
    user_id: int
    schemas: PurchasedItemSchemas
    scopes: PurchasedItemScopes
    filter: type[PurchasedItemFilter]
    sort: type[PurchasedItemSort]

class PurchasedItemSchemas:
    """Schemas for the PurchasedItem model."""

    create: PurchasedItemSchemaCreate
    update: PurchasedItemSchemaUpdate
    response: PurchasedItemSchemaResponse

class PurchasedItemSchemaCreate(AwesomeBaseModel):
    """create schema for PurchasedItem model"""

    user_id: Optional[int]
    service_id: Optional[int]
    transaction_id: Optional[int]
    status: Optional[PurchasedItemStatus]
    quantity: Optional[int]
    expires_at: Optional[datetime]
    purchase_metadata: Optional[dict[str, Any]]
    user: Optional[User]
    service: Optional[Service]
    transaction: Optional[Transaction]

class PurchasedItemSchemaUpdate(AwesomeBaseModel):
    """update schema for PurchasedItem model"""

    user_id: Optional[int]
    service_id: Optional[int]
    transaction_id: Optional[int]
    status: Optional[PurchasedItemStatus]
    quantity: Optional[int]
    expires_at: Optional[datetime]
    purchase_metadata: Optional[dict[str, Any]]
    user: Optional[User]
    service: Optional[Service]
    transaction: Optional[Transaction]

class PurchasedItemSchemaResponse(AwesomeBaseModel):
    """response schema for PurchasedItem model"""

    updated_at: datetime
    id: int
    user_id: int
    service_id: int
    transaction_id: int
    status: PurchasedItemStatus
    quantity: int
    expires_at: Optional[datetime]
    purchase_metadata: Optional[dict[str, Any]]
    user: Optional[User]
    service: Optional[Service]
    transaction: Optional[Transaction]

class PurchasedItemScopes:
    """Scopes for the PurchasedItem model."""

class PurchasedItemFilter(BaseModel):
    """Pydantic-class for filtering the PurchasedItem model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    service_id: Optional[int] = None
    min_service_id: Optional[Any] = None
    max_service_id: Optional[Any] = None
    transaction_id: Optional[int] = None
    min_transaction_id: Optional[Any] = None
    max_transaction_id: Optional[Any] = None
    status: Optional[PurchasedItemStatus] = None
    quantity: Optional[int] = None
    min_quantity: Optional[Any] = None
    max_quantity: Optional[Any] = None
    expires_at: Optional[datetime] = None
    min_expires_at: Optional[Any] = None
    max_expires_at: Optional[Any] = None
    service_name: Optional[Any] = None

class PurchasedItemSort(StrEnum):
    """Enum for sorting the PurchasedItem model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
