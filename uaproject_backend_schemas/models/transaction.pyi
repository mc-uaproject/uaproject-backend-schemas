# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.transaction import TransactionType
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.user import User

class Transaction(AwesomeModel):
    """Base transaction model."""

    amount: Decimal
    description: Optional[str]
    id: int
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
    scopes: TransactionScopes
    filter: type[TransactionFilter]
    sort: type[TransactionSort]

class TransactionSchemas:
    """Schemas for the Transaction model."""

    create: TransactionSchemaCreate
    update: TransactionSchemaUpdate
    response: TransactionSchemaResponse

class TransactionSchemaCreate(AwesomeBaseModel):
    """create schema for Transaction model"""

    user_id: Optional[int]
    amount: Optional[Decimal]
    type: Optional[TransactionType]
    description: Optional[str]
    recipient_id: Optional[int]
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    service: Optional[Service]
    user: Optional[User]
    recipient: Optional[User]

class TransactionSchemaUpdate(AwesomeBaseModel):
    """update schema for Transaction model"""

    user_id: Optional[int]
    amount: Optional[Decimal]
    type: Optional[TransactionType]
    description: Optional[str]
    recipient_id: Optional[int]
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    service: Optional[Service]
    user: Optional[User]
    recipient: Optional[User]

class TransactionSchemaResponse(AwesomeBaseModel):
    """response schema for Transaction model"""

    updated_at: datetime
    id: int
    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[dict[str, Any]]
    service: Optional[Service]
    user: Optional[User]
    recipient: Optional[User]

class TransactionScopes:
    """Scopes for the Transaction model."""

class TransactionFilter(BaseModel):
    """Pydantic-class for filtering the Transaction model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    description: Optional[str] = None
    recipient_id: Optional[int] = None
    min_recipient_id: Optional[Any] = None
    max_recipient_id: Optional[Any] = None
    service_id: Optional[int] = None
    min_service_id: Optional[Any] = None
    max_service_id: Optional[Any] = None

class TransactionSort(StrEnum):
    """Enum for sorting the Transaction model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
