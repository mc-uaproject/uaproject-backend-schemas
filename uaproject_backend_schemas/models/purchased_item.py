from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import ARRAY, JSON, BigInteger, Column, DateTime, Enum, ForeignKey, String
from sqlmodel import Field, Relationship

from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.purchased_item import PurchasedItemStatus

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.service import Service
    from uaproject_backend_schemas.models.transaction import Transaction
    from uaproject_backend_schemas.models.user import User


class PurchasedItem(
    AwesomeModel,
    IDMixin,
    TimestampsMixin,
    table=True,
):
    __tablename__ = "purchased_items"
    __scope_prefix__ = "purchased_item"

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False))
    service_id: int = Field(
        sa_column=Column(BigInteger(), ForeignKey("services.id"), nullable=False)
    )
    transaction_id: int = Field(
        sa_column=Column(BigInteger(), ForeignKey("transactions.id"), nullable=False)
    )
    status: PurchasedItemStatus = Field(
        sa_column=Column(
            Enum(PurchasedItemStatus, native_enum=False),
            default=PurchasedItemStatus.ACTIVE.value,
            server_default=PurchasedItemStatus.ACTIVE.value,
        )
    )
    quantity: int = Field(default=1, ge=1)
    expires_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    servers: List[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False),
        description="List of servers where this purchase is active"
    )
    purchase_metadata: Optional[Dict[str, Any]] = Field(sa_column=Column(JSON), default=None)

    user: Optional["User"] = Relationship(back_populates="purchased_items")
    service: Optional["Service"] = Relationship(back_populates="purchased_items")
    transaction: Optional["Transaction"] = Relationship(back_populates="purchased_item")
