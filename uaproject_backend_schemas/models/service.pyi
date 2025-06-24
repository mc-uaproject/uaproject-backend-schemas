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
    scopes: ServiceScopes
    filter: type[ServiceFilter]
    sort: type[ServiceSort]

class ServiceSchemas:
    """Schemas for the Service model."""

    create: ServiceSchemaCreate
    update: ServiceSchemaUpdate
    response: ServiceSchemaResponse

class ServiceSchemaCreate(AwesomeBaseModel):
    """create schema for Service model"""

    name: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[list[ServicePoint]]
    image: Optional[str]
    price: Optional[Decimal]
    is_active: Optional[bool]
    category: Optional[str]
    type: Optional[ServiceType]
    duration_months: Optional[int]
    is_upgradable: Optional[bool]
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[dict[str, Any]]
    discounts: Optional[list[ServiceDiscount]]
    icon_file: Optional[File]
    purchased_items: Optional[list[PurchasedItem]]

class ServiceSchemaUpdate(AwesomeBaseModel):
    """update schema for Service model"""

    name: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[list[ServicePoint]]
    image: Optional[str]
    price: Optional[Decimal]
    is_active: Optional[bool]
    category: Optional[str]
    type: Optional[ServiceType]
    duration_months: Optional[int]
    is_upgradable: Optional[bool]
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[dict[str, Any]]
    discounts: Optional[list[ServiceDiscount]]
    icon_file: Optional[File]
    purchased_items: Optional[list[PurchasedItem]]

class ServiceSchemaResponse(AwesomeBaseModel):
    """response schema for Service model"""

    updated_at: datetime
    id: int
    name: str
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[list[ServicePoint]]
    image: Optional[str]
    price: Decimal
    is_active: bool
    category: Optional[str]
    type: ServiceType
    duration_months: Optional[int]
    is_upgradable: bool
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[dict[str, Any]]
    discounts: Optional[list[ServiceDiscount]]
    icon_file: Optional[File]
    purchased_items: list[PurchasedItem]

class ServiceScopes:
    """Scopes for the Service model."""

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

class ServiceSort(StrEnum):
    """Enum for sorting the Service model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
