# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.transaction import TransactionType
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.user import User

class Transaction(AwesomeModel):
    """Base user model."""

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
    schemas: TransactionSchemas
    scopes: TransactionScopes
    filters: TransactionFilters
    filter: type[TransactionFilter]

class TransactionSchemas:
    """Schemas for the Transaction model."""

class TransactionScopes:
    """Scopes for the Transaction model."""

class TransactionFilters:
    """Declarative filters for the Transaction model."""

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
    transaction_metadata: Optional[Dict] = None
