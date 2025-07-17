# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

class Balance(AwesomeModel):
    """Base balance model."""

    amount: Decimal
    created_at: datetime
    id: int
    identifier: UUID
    updated_at: datetime
    user: User
    user_id: int
    schemas: BalanceSchemas
    filter: type[BalanceFilter]
    sort: type[BalanceSort]

class BalanceSchemas:
    """Schemas for the Balance model."""

    create: BalanceSchemaCreate
    redis: BalanceSchemaRedis
    response: BalanceSchemaResponse
    response_self: BalanceSchemaResponseSelf
    update: BalanceSchemaUpdate

class BalanceSchemaCreate(AwesomeBaseModel):
    """create schema for Balance model"""

    amount: Optional[Decimal]
    user_id: int

class BalanceSchemaRedis(AwesomeBaseModel):
    """redis schema for Balance model"""

    user: Optional[User]
    identifier: Optional[UUID]
    updated_at: Optional[datetime]
    id: Optional[int]
    amount: Optional[Decimal]
    user_id: Optional[int]
    created_at: datetime

class BalanceSchemaResponse(AwesomeBaseModel):
    """response schema for Balance model"""

    identifier: Optional[UUID]
    updated_at: Optional[datetime]
    id: Optional[int]
    amount: Optional[Decimal]
    user_id: int
    created_at: datetime

class BalanceSchemaResponseSelf(AwesomeBaseModel):
    """response_self schema for Balance model"""

    identifier: Optional[UUID]
    updated_at: Optional[datetime]
    id: Optional[int]
    amount: Optional[Decimal]
    user_id: int
    created_at: datetime

class BalanceSchemaUpdate(AwesomeBaseModel):
    """update schema for Balance model"""

    id: Optional[int]
    amount: Optional[Decimal]

class BalanceFilter(BaseModel):
    """Pydantic-class for filtering the Balance model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    identifier: Optional[UUID] = None
    amount: Optional[Decimal] = None

class BalanceSort(StrEnum):
    """Enum for sorting the Balance model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
