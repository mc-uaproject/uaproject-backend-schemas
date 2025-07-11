from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlmodel import DECIMAL, JSON, Column, Enum, Index, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.service import (
    ServerAvailability,
    ServiceDiscount,
    ServicePoint,
    ServiceType,
)

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.file import File
    from uaproject_backend_schemas.models.purchased_item import PurchasedItem


class Service(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "services"
    __scope_prefix__ = "service"
    __table_args__ = (
        Index("ix_services_active", "is_active"),
        Index("ix_services_category", "category"),
        Index("ix_services_type", "type"),
        Index("ix_services_name", "name"),
        Index("ix_services_price", "price"),
    )
    name: str = AwesomeField(max_length=255, unique=True, nullable=False)
    display_name: Optional[str] = AwesomeField(max_length=255, nullable=True)
    description: Optional[str] = AwesomeField(max_length=1000, nullable=True)
    points: Optional[List[ServicePoint]] = AwesomeField(sa_column=Column(JSON), default=None)
    image: Optional[str] = AwesomeField(max_length=500, nullable=True)
    price: Decimal = AwesomeField(sa_column=Column(DECIMAL(10, 2), nullable=False))
    is_active: bool = AwesomeField(default=True)
    category: Optional[str] = AwesomeField(max_length=100, nullable=True)
    type: ServiceType = AwesomeField(
        sa_column=Column(Enum(ServiceType, native_enum=False), nullable=False)
    )
    duration_months: Optional[int] = AwesomeField(nullable=True)
    is_upgradable: bool = AwesomeField(default=False)
    upgrade_from: Optional[str] = AwesomeField(max_length=100, nullable=True)
    upgrade_to: Optional[str] = AwesomeField(max_length=100, nullable=True)
    service_metadata: Optional[Dict[str, Any]] = AwesomeField(sa_column=Column(JSON), default=None)
    discounts: Optional[List[ServiceDiscount]] = AwesomeField(sa_column=Column(JSON), default=None)
    server_availability: Optional[ServerAvailability] = AwesomeField(
        sa_column=Column(JSON),
        default=None,
        description="Configuration for service availability across servers",
    )

    # MinIO file relationship (one-to-one)
    icon_file: Optional["File"] = Relationship(back_populates="service")
    purchased_items: List["PurchasedItem"] = Relationship(
        back_populates="service",
        sa_relationship_kwargs={"foreign_keys": "[PurchasedItem.service_id]"},
    )
