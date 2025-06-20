# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Balance(AwesomeModel):
    """Base balance model."""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal
    created_at: datetime
    user: Optional[User]
    schemas: BalanceSchemas
    scopes: BalanceScopes
    filter: type[BalanceFilter]
    sort: type[BalanceSort]

class BalanceSchemas:
    """Schemas for the Balance model."""

    create: BalanceSchemaCreate
    update: BalanceSchemaUpdate
    response: BalanceSchemaResponse
    response_self: BalanceSchemaResponseSelf

class BalanceSchemaCreate(AwesomeBaseModel):
    """create schema for Balance model"""

    amount: Decimal
    user: Optional[User]

class BalanceSchemaUpdate(AwesomeBaseModel):
    """update schema for Balance model"""

    amount: Decimal

class BalanceSchemaResponse(AwesomeBaseModel):
    """response schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal
    user: Optional[User]

class BalanceSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for Balance model"""

    updated_at: datetime
    id: int
    user_id: int
    identifier: UUID
    amount: Decimal
    user: Optional[User]

class BalanceScopes:
    """Scopes for the Balance model."""

    amount: BalanceScopeAmount

class BalanceScopeAmount(AwesomeBaseModel):
    """amount schema for Balance model"""

    id: int
    user_id: int
    amount: Decimal

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

class BalanceSort(StrEnum):
    """Enum for sorting the Balance model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
