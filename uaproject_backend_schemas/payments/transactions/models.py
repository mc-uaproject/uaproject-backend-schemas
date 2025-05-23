from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlmodel import DECIMAL, JSON, BigInteger, Column, Enum, Field, ForeignKey, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.payments.services.models import Service
from uaproject_backend_schemas.payments.services.schemas import ServiceResponse
from uaproject_backend_schemas.payments.transactions.payload import TransactionCreatedPayload
from uaproject_backend_schemas.payments.transactions.schemas import TransactionType
from uaproject_backend_schemas.schemas import SerializableDecimal
from uaproject_backend_schemas.webhooks.mixins import (
    WebhookActionsMixin,
    WebhookChangesMixin,
    WebhookRelationshipsMixin,
)
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User


__all__ = ["Transaction"]


class Transaction(
    TimestampsMixin,
    IDMixin,
    Base,
    WebhookChangesMixin,
    WebhookActionsMixin,
    WebhookRelationshipsMixin,
    table=True,
):
    __tablename__ = "transactions"
    __scope_prefix__ = "transaction"

    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False))
    amount: SerializableDecimal = Field(sa_column=Column(DECIMAL(10, 2), nullable=False))
    type: TransactionType = Field(sa_column=Column(Enum(TransactionType, native_enum=False)))
    description: Optional[str] = Field(max_length=255, nullable=True)
    recipient_id: int = Field(
        sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=False)
    )
    service_id: Optional[int] = Field(
        sa_column=Column(BigInteger(), ForeignKey("services.id"), nullable=True)
    )
    transaction_metadata: Optional[Dict[str, Any]] = Field(sa_column=Column(JSON, nullable=True))

    service: Optional["Service"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Transaction.service_id]"}
    )
    user: Optional["User"] = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.user_id]"},
    )
    recipient: Optional["User"] = Relationship(
        back_populates="received_transactions",
        sa_relationship_kwargs={"foreign_keys": "[Transaction.recipient_id]"},
    )

    @classmethod
    def register_scopes(cls) -> None:
        cls.register_scope(
            "created",
            trigger_fields={
                "user_id",
                "amount",
                "type",
                "description",
                "recipient_id",
                "service_id",
            },
            fields=TransactionCreatedPayload.model_construct(),
            relationships={
                "service": {
                    "fields": ServiceResponse.model_construct(),
                    "condition": "service_id",
                    "condition_value": None,
                    "condition_operator": "is not",
                },
            },
            stage=WebhookStage.AFTER,
        )
        cls.register_scope(
            "type",
            trigger_fields={"type"},
            fields={"id", "user_id", "amount", "type", "description"},
            stage=WebhookStage.BOTH,
        )
        cls.register_scope(
            "amount",
            trigger_fields={"amount"},
            fields={"id", "user_id", "amount", "type", "description"},
            stage=WebhookStage.BOTH,
        )
        cls.register_scope(
            "purchase_flow",
            trigger_fields={"type", "service_id", "amount"},
            fields={
                "id",
                "user_id",
                "recipient_id",
                "amount",
                "type",
                "service_id",
                "transaction_metadata",
            },
            relationships={
                "service": {
                    "fields": ServiceResponse.model_construct(),
                    "condition": "type",
                    "condition_value": TransactionType.PURCHASE,
                    "condition_operator": "==",
                },
            },
            stage=WebhookStage.AFTER,
            actions=[
                {
                    "type": "update_balance",
                    "user_id": "recipient_id",
                    "amount": "amount",
                },
                {
                    "type": "create_or_update_purchased_item",
                    "condition": "type == TransactionType.PURCHASE",
                    "fields": {
                        "user_id": "recipient_id",
                        "service_id": "service_id",
                        "transaction_id": "id",
                        "status": "ACTIVE",
                        "quantity": 1,
                    },
                },
            ],
        )
