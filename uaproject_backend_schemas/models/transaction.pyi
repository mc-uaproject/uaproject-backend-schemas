# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
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

class TransactionSchemas:
    """Schemas for the user model."""

    create: TransactionSchemaCreate
    update: TransactionSchemaUpdate
    response: TransactionSchemaResponse

class TransactionScopes:
    """Visibility scopes for the user model."""

    full: TransactionScopeFull

class TransactionSchemaCreate(AwesomeBaseModel):
    """Create schema for Transaction model"""

    updated_at: datetime
    id: int
    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]

class TransactionSchemaUpdate(AwesomeBaseModel):
    """Update schema for Transaction model"""

    updated_at: datetime
    id: int
    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]

class TransactionSchemaResponse(AwesomeBaseModel):
    """Response schema for Transaction model"""

    updated_at: datetime
    id: int
    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]

class TransactionScopeFull(AwesomeBaseModel):
    """full visibility scope for Transaction model"""

    updated_at: datetime
    id: int
    user_id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    recipient_id: int
    service_id: Optional[int]
    transaction_metadata: Optional[Dict]
