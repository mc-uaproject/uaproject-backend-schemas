from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import BigInteger, Column, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.scopes import ScopeDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User


class Balance(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "balances"
    __scope_prefix__ = "balance"
    model_config = {"arbitrary_types_allowed": True}

    user_id: int = AwesomeField(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False, unique=True)
    )
    identifier: UUID = AwesomeField(default_factory=uuid4, nullable=False, unique=True)
    amount: Decimal = AwesomeField(default=0, nullable=False)

    user: "User" = Relationship(back_populates="balance")

    class Amount(ScopeDefinition):
        trigger_fields = ["amount"]
        fields = ["id", "user_id", "amount"]
        permissions = ["read"]
