from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlmodel import DECIMAL, JSON, Column, Enum

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.service import (
    ServiceDiscount,
    ServicePoint,
    ServiceType,
)


class Service(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "services"
    __scope_prefix__ = "service"
    name: str = AwesomeField(max_length=255, unique=True, nullable=False)
    display_name: Optional[str] = AwesomeField(max_length=255, nullable=True)
    description: Optional[str] = AwesomeField(max_length=1000, nullable=True)
    points: Optional[List[ServicePoint]] = AwesomeField(sa_column=Column(JSON), default=None)
    image: Optional[str] = AwesomeField(max_length=500, nullable=True)
    price: Decimal = AwesomeField(sa_column=Column(DECIMAL(10, 2), nullable=False))
    is_active: bool = AwesomeField(default=True)
    category: Optional[str] = AwesomeField(max_length=100, nullable=True)
    type: ServiceType = AwesomeField(sa_column=Column(Enum(ServiceType, native_enum=False)))
    duration_months: Optional[int] = AwesomeField(nullable=True)
    is_upgradable: bool = AwesomeField(default=False)
    upgrade_from: Optional[str] = AwesomeField(max_length=100, nullable=True)
    upgrade_to: Optional[str] = AwesomeField(max_length=100, nullable=True)
    service_metadata: Optional[Dict[str, Any]] = AwesomeField(sa_column=Column(JSON), default=None)
    discounts: Optional[List[ServiceDiscount]] = AwesomeField(sa_column=Column(JSON), default=None)
