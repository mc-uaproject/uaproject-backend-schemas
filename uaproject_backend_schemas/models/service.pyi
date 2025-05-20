# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.service import (
    ServiceType,
)

class Service(AwesomeModel):
    """Base user model."""

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
    schemas: ServiceSchemas
    scopes: ServiceScopes

class ServiceSchemas:
    """Schemas for the user model."""

    create: ServiceSchemaCreate
    update: ServiceSchemaUpdate
    response: ServiceSchemaResponse

class ServiceScopes:
    """Visibility scopes for the user model."""

    full: ServiceScopeFull

class ServiceSchemaCreate(AwesomeBaseModel):
    """Create schema for Service model"""

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

class ServiceSchemaUpdate(AwesomeBaseModel):
    """Update schema for Service model"""

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

class ServiceSchemaResponse(AwesomeBaseModel):
    """Response schema for Service model"""

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

class ServiceScopeFull(AwesomeBaseModel):
    """full visibility scope for Service model"""

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
