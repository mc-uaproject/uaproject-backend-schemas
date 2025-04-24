import logging
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from uaproject_backend_schemas.payments.purchases.models import PurchasedItem
from uaproject_backend_schemas.payments.purchases.schemas import PurchasedItemStatus
from uaproject_backend_schemas.payments.transactions.models import Transaction
from uaproject_backend_schemas.payments.transactions.schemas import TransactionType
from uaproject_backend_schemas.users.models import User

logger = logging.getLogger(__name__)


async def update_balance_handler(instance: Transaction, action_config: Dict[str, Any]) -> None:
    """Handler for updating user balance"""
    session: AsyncSession = instance._sa_instance_state.session
    user_id = getattr(instance, action_config["user_id"])
    amount = getattr(instance, action_config["amount"])

    user = await session.get(User, user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        return

    user.balance += amount
    session.add(user)
    await session.commit()


async def create_or_update_purchased_item_handler(
    instance: Transaction, action_config: Dict[str, Any]
) -> None:
    """Handler for creating or updating purchased item"""
    if instance.type != TransactionType.PURCHASE:
        return

    session: AsyncSession = instance._sa_instance_state.session
    fields = action_config["fields"]

    # Get or create purchased item
    purchased_item = await session.get(
        PurchasedItem,
        {
            "user_id": getattr(instance, fields["user_id"]),
            "service_id": getattr(instance, fields["service_id"]),
            "transaction_id": getattr(instance, fields["transaction_id"]),
        },
    )

    if not purchased_item:
        purchased_item = PurchasedItem(
            user_id=getattr(instance, fields["user_id"]),
            service_id=getattr(instance, fields["service_id"]),
            transaction_id=getattr(instance, fields["transaction_id"]),
            status=PurchasedItemStatus.ACTIVE,
            quantity=fields["quantity"],
        )
        session.add(purchased_item)
    else:
        purchased_item.status = PurchasedItemStatus.ACTIVE
        purchased_item.quantity += fields["quantity"]

    await session.commit()


def register_action_handlers() -> None:
    """Register all action handlers"""
    Transaction.register_action_handler("update_balance", update_balance_handler)
    Transaction.register_action_handler(
        "create_or_update_purchased_item", create_or_update_purchased_item_handler
    )
