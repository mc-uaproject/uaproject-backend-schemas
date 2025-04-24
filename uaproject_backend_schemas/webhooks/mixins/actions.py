import logging
from typing import Any, Dict, List

from uaproject_backend_schemas.webhooks.mixins.base import WebhookBaseMixin
from uaproject_backend_schemas.webhooks.mixins.config import ActionConfigModel
from uaproject_backend_schemas.webhooks.types import ActionConfig, ActionHandler

logger = logging.getLogger(__name__)

__all__ = ["WebhookActionsMixin"]


class WebhookActionsMixin(WebhookBaseMixin):
    """Mixin for handling webhook actions"""

    _action_handlers: Dict[str, ActionHandler] = {}

    @classmethod
    def register_action_handler(cls, action_type: str, handler: ActionHandler) -> None:
        """
        Register a handler for a specific action type

        Args:
            action_type: The type of action to handle
            handler: A function that takes (instance, action_config) as parameters
        """
        cls._action_handlers[action_type] = handler

    @classmethod
    def _process_actions(cls, actions: List[ActionConfig]) -> List[ActionConfigModel]:
        """Process and validate action configurations"""
        return [ActionConfigModel(**action) for action in actions]

    async def execute_actions(self, scope_name: str) -> None:
        """Execute actions for the specified scope"""
        scopes = self.__class__.get_webhook_scopes()
        scope_config = scopes.get(scope_name)

        if not scope_config or not scope_config.actions:
            return

        for action in scope_config.actions:
            if action.condition and not self._evaluate_condition(
                getattr(self, action.condition), True, "=="
            ):
                continue

            handler = self._action_handlers.get(action.type)
            if handler:
                try:
                    await handler(self, action.model_dump())
                except Exception as e:
                    logger.error(f"Error executing action {action.type}: {e}", exc_info=True)
            else:
                logger.warning(f"No handler registered for action type: {action.type}")

    def _evaluate_condition(
        self, field_value: Any, condition_value: Any, condition_operator: str
    ) -> bool:
        """Evaluate the condition based on the operator"""
        operators = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "is": lambda a, b: a is b,
            "is not": lambda a, b: a is not b,
        }

        try:
            operator_func = operators.get(condition_operator)
            if not operator_func:
                logger.warning(f"Unknown condition operator: {condition_operator}")
                return False

            return operator_func(field_value, condition_value)

        except TypeError as e:
            logger.error(
                f"Condition check failed for field with value '{field_value}' "
                f"and condition value '{condition_value}': {e}"
            )
            return False
