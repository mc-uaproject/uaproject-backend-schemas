# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel
from uaproject_backend_schemas.models.service import ServiceType

class Service(AwesomeModel):
    """Base user model."""

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
    """create schema for Service model"""

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
    """update schema for Service model"""

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
