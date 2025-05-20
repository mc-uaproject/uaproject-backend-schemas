# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

class Balance(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal
    schemas: BalanceSchemas
    scopes: BalanceScopes

class BalanceSchemas:
    """Schemas for the user model."""

    create: BalanceSchemaCreate
    update: BalanceSchemaUpdate
    response: BalanceSchemaResponse

class BalanceScopes:
    """Visibility scopes for the user model."""

    full: BalanceScopeFull

class BalanceSchemaCreate(AwesomeBaseModel):
    """Create schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal

class BalanceSchemaUpdate(AwesomeBaseModel):
    """Update schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal

class BalanceSchemaResponse(AwesomeBaseModel):
    """Response schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal

class BalanceScopeFull(AwesomeBaseModel):
    """full visibility scope for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal
