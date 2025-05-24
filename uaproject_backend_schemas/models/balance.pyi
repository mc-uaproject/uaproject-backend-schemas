# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Balance(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal
    user: Optional[User]
    schemas: BalanceSchemas
    scopes: BalanceScopes
    filters: BalanceFilters
    filter: type[BalanceFilter]

class BalanceSchemas:
    """Schemas for the user model."""

    create: BalanceSchemaCreate
    update: BalanceSchemaUpdate
    response: BalanceSchemaResponse

class BalanceScopes:
    """Visibility scopes for the user model."""

    full: BalanceScopeFull

class BalanceFilters:
    """Declarative filters for the Balance model."""

class BalanceFilter(BaseModel):
    """Pydantic-class for filtering the Balance model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    identifier: Optional[UUID] = None
    amount: Optional[Decimal] = None

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
