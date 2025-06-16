# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.service import (
    ServiceType,
)

class Service(AwesomeModel):
    """Base service model."""

    updated_at: datetime
    id: int
    name: str
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[List]
    image: Optional[str]
    price: Decimal
    is_active: bool
    category: Optional[str]
    type: ServiceType
    duration_months: Optional[int]
    is_upgradable: bool
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[Dict]
    discounts: Optional[List]
    created_at: datetime
    schemas: ServiceSchemas
    scopes: ServiceScopes
    filters: ServiceFilters
    sorts: ServiceSorts
    filter: type[ServiceFilter]
    sort: type[ServiceSort]

class ServiceSchemas:
    """Schemas for the Service model."""

    create: ServiceSchemaCreate
    update: ServiceSchemaUpdate
    response: ServiceSchemaResponse

class ServiceSchemaCreate(AwesomeBaseModel):
    """create schema for Service model"""

    name: str
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[List]
    image: Optional[str]
    price: Decimal
    is_active: bool
    category: Optional[str]
    type: ServiceType
    duration_months: Optional[int]
    is_upgradable: bool
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[Dict]
    discounts: Optional[List]

class ServiceSchemaUpdate(AwesomeBaseModel):
    """update schema for Service model"""

    name: str
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[List]
    image: Optional[str]
    price: Decimal
    is_active: bool
    category: Optional[str]
    type: ServiceType
    duration_months: Optional[int]
    is_upgradable: bool
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[Dict]
    discounts: Optional[List]

class ServiceSchemaResponse(AwesomeBaseModel):
    """response schema for Service model"""

    updated_at: datetime
    id: int
    name: str
    display_name: Optional[str]
    description: Optional[str]
    points: Optional[List]
    image: Optional[str]
    price: Decimal
    is_active: bool
    category: Optional[str]
    type: ServiceType
    duration_months: Optional[int]
    is_upgradable: bool
    upgrade_from: Optional[str]
    upgrade_to: Optional[str]
    service_metadata: Optional[Dict]
    discounts: Optional[List]

class ServiceScopes:
    """Scopes for the Service model."""

class ServiceFilters:
    """Declarative filters for the Service model."""

class ServiceFilter(BaseModel):
    """Pydantic-class for filtering the Service model."""

class ServiceSorts:
    """Declarative sorts for the Service model."""

class ServiceSort(StrEnum):
    """Enum for sorting the Service model."""
