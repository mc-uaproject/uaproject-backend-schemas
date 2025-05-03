# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel

class Balance(AwesomeModel):
    """Base user model."""

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
    """create schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal

class BalanceSchemaUpdate(AwesomeBaseModel):
    """update schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal

class BalanceSchemaResponse(AwesomeBaseModel):
    """response schema for Balance model"""

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
