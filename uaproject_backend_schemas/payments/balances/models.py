from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import DECIMAL, Column
from sqlmodel import Field, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["Balance"]

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User


class Balance(TimestampsMixin, IDMixin, Base, WebhookPayloadMixin, table=True):
    __tablename__ = "balances"
    __scope_prefix__ = "balance"

    user_id: int = Field(foreign_key="users.id", nullable=False, unique=True)
    identifier: UUID = Field(default_factory=uuid4, nullable=False, unique=True)
    amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    user: Optional["User"] = Relationship(
        back_populates="balance", sa_relationship_kwargs={"uselist": False}
    )

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "amount",
            trigger_fields={"amount"},
            fields={"id", "user_id", "amount", "identifier"},
            stage=WebhookStage.BOTH,
        )

        cls.register_scope(
            "full", trigger_fields={"user_id", "amount", "identifier"}, stage=WebhookStage.AFTER
        )
