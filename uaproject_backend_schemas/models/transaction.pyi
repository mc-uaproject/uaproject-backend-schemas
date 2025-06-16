# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Dict, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.transaction import TransactionType
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.user import User

class Transaction(AwesomeModel):
    """Base transaction model."""

    updated_at: datetime
    id: int
    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]
    created_at: datetime
    service: Optional[Service]
    user: Optional[User]
    recipient: Optional[User]
    schemas: TransactionSchemas
    scopes: TransactionScopes
    filters: TransactionFilters
    sorts: TransactionSorts
    filter: type[TransactionFilter]
    sort: type[TransactionSort]

class TransactionSchemas:
    """Schemas for the Transaction model."""

    create: TransactionSchemaCreate
    update: TransactionSchemaUpdate
    response: TransactionSchemaResponse

class TransactionSchemaCreate(AwesomeBaseModel):
    """create schema for Transaction model"""

    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]
    service: Optional[Service]
    user: Optional[User]
    recipient: Optional[User]

class TransactionSchemaUpdate(AwesomeBaseModel):
    """update schema for Transaction model"""

    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]
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
    transaction_metadata: Optional[Dict]
    service: Optional[Service]
    user: Optional[User]
    recipient: Optional[User]

class TransactionScopes:
    """Scopes for the Transaction model."""

class TransactionFilters:
    """Declarative filters for the Transaction model."""

class TransactionFilter(BaseModel):
    """Pydantic-class for filtering the Transaction model."""

class TransactionSorts:
    """Declarative sorts for the Transaction model."""

class TransactionSort(StrEnum):
    """Enum for sorting the Transaction model."""
