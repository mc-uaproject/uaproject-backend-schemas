# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.purchased_item import PurchasedItem
from uaproject_backend_schemas.models.schemas.service import (
    ServiceDiscount,
    ServicePoint,
    ServiceType,
)

class Service(AwesomeModel):
    """Base service model."""

    category: Optional[str]
    created_at: datetime
    description: Optional[str]
    discounts: Optional[list[ServiceDiscount]]
    display_name: Optional[str]
    duration_months: Optional[int]
    icon_file: Optional[File]
    id: int
    image: Optional[str]
    is_active: bool
    is_upgradable: bool
    name: str
    points: Optional[list[ServicePoint]]
    price: Decimal
    purchased_items: list[PurchasedItem]
    service_metadata: Optional[dict[str, Any]]
    type: ServiceType
    updated_at: datetime
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    schemas: ServiceSchemas
    filter: type[ServiceFilter]
    sort: type[ServiceSort]

class ServiceSchemas:
    """Schemas for the Service model."""

    create: ServiceSchemaCreate
    redis: ServiceSchemaRedis
    response: ServiceSchemaResponse
    update: ServiceSchemaUpdate

class ServiceSchemaCreate(AwesomeBaseModel):
    """create schema for Service model"""

    points: Optional[list[ServicePoint]]
    price: Optional[Decimal]
    is_active: Optional[bool]
    discounts: Optional[list[ServiceDiscount]]
    type: Optional[ServiceType]
    upgrade_from: Optional[str]
    duration_months: Optional[int]
    image: Optional[str]
    display_name: Optional[str]
    is_upgradable: Optional[bool]
    description: Optional[str]
    service_metadata: Optional[dict[str, Any]]
    name: Optional[str]
    upgrade_to: Optional[str]
    category: Optional[str]

class ServiceSchemaRedis(AwesomeBaseModel):
    """redis schema for Service model"""

    price: Optional[Decimal]
    service_metadata: Optional[dict[str, Any]]
    category: Optional[str]
    points: Optional[list[ServicePoint]]
    image: Optional[str]
    is_upgradable: Optional[bool]
    type: Optional[ServiceType]
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    purchased_items: Optional[list[PurchasedItem]]
    updated_at: Optional[datetime]
    duration_months: Optional[int]
    discounts: Optional[list[ServiceDiscount]]
    created_at: Optional[datetime]
    description: Optional[str]
    name: Optional[str]
    icon_file: Optional[File]
    is_active: Optional[bool]
    display_name: Optional[str]
    id: Optional[int]

class ServiceSchemaResponse(AwesomeBaseModel):
    """response schema for Service model"""

    points: Optional[list[ServicePoint]]
    price: Decimal
    created_at: Optional[datetime]
    is_active: Optional[bool]
    discounts: Optional[list[ServiceDiscount]]
    type: ServiceType
    upgrade_from: Optional[str]
    updated_at: Optional[datetime]
    duration_months: Optional[int]
    image: Optional[str]
    display_name: Optional[str]
    is_upgradable: Optional[bool]
    description: Optional[str]
    service_metadata: Optional[dict[str, Any]]
    id: Optional[int]
    name: str
    upgrade_to: Optional[str]
    category: Optional[str]

class ServiceSchemaUpdate(AwesomeBaseModel):
    """update schema for Service model"""

    points: Optional[list[ServicePoint]]
    price: Optional[Decimal]
    is_active: Optional[bool]
    discounts: Optional[list[ServiceDiscount]]
    type: Optional[ServiceType]
    upgrade_from: Optional[str]
    duration_months: Optional[int]
    image: Optional[str]
    display_name: Optional[str]
    is_upgradable: Optional[bool]
    description: Optional[str]
    service_metadata: Optional[dict[str, Any]]
    name: Optional[str]
    upgrade_to: Optional[str]
    category: Optional[str]

class ServiceFilter(BaseModel):
    """Pydantic-class for filtering the Service model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    price: Optional[Decimal] = None
    is_active: Optional[bool] = None
    category: Optional[str] = None
    type: Optional[ServiceType] = None
    duration_months: Optional[int] = None
    min_duration_months: Optional[Any] = None
    max_duration_months: Optional[Any] = None
    is_upgradable: Optional[bool] = None
    upgrade_from: Optional[str] = None
    upgrade_to: Optional[str] = None
    icon_file_id: Optional[Any] = None
    purchased_items_id: Optional[Any] = None

class ServiceSort(StrEnum):
    """Enum for sorting the Service model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
