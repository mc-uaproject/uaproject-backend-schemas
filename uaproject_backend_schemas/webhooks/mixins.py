from typing import Any, Dict, List, Literal, Optional, Set, Union

from pydantic import BaseModel
from sqlalchemy import inspect

from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["WebhookScopeFields", "PayloadType", "WebhookPayloadMixin"]


class WebhookScopeFields(BaseModel):
    trigger_fields: List[str]
    fields: Optional[List[str]] = None
    stage: WebhookStage = WebhookStage.AFTER


PayloadType = Union[Dict[str, Any], Dict[Literal["before", "after"], Dict[str, Any]]]


class WebhookPayloadMixin:
    """A mixin that adds webhook functionality to a model"""

    __scope_prefix__ = ""

    @classmethod
    def get_webhook_scopes(cls) -> Dict[str, WebhookScopeFields]:
        """Get webhook scopes for this specific class"""
        if not hasattr(cls, "_webhook_scopes_registry"):
            cls._webhook_scopes_registry = {}
        return cls._webhook_scopes_registry

    @classmethod
    def register_scope(
        cls,
        scope_name: str,
        trigger_fields: List[str] | Set[str],
        fields: List[str] | Set[str] | None = None,
        stage: WebhookStage = WebhookStage.AFTER,
    ) -> None:
        """
        Register a new scope for the model with specified
        trigger fields and optional payload fields.

        Args:
            scope_name: Unique identifier for the scope
            trigger_fields: Fields that will trigger the webhook when modified
            fields: Optional specific fields to include in the payload.
                   If None, all fields will be included.
            stage: WebhookStage indicating when the webhook should be triggered
                  and what data should be included in the payload
        """
        scope_name = f"{cls.__scope_prefix__}.{scope_name}"
        scopes = cls.get_webhook_scopes()

        if scope_name in scopes:
            raise ValueError(f"Scope '{scope_name}' is already registered for {cls.__name__}")

        trigger_fields_set = set(trigger_fields)
        fields_set = set(fields) if fields is not None else None

        model_fields = set(cls.__table__.columns.keys())
        if invalid_triggers := trigger_fields_set - model_fields:
            raise ValueError(f"Invalid trigger fields for {cls.__name__}: {invalid_triggers}")

        if fields_set is not None:
            if invalid_fields := fields_set - model_fields:
                raise ValueError(f"Invalid payload fields for {cls.__name__}: {invalid_fields}")

        scopes[scope_name] = WebhookScopeFields(
            trigger_fields=list(trigger_fields_set),
            fields=list(fields_set) if fields_set else None,
            stage=stage,
        )

    def is_webhook_triggered(self, scope_name: str) -> bool:
        """Check if the webhook should be triggered for the specified scope"""
        scopes = self.__class__.get_webhook_scopes()
        scope_config = scopes.get(scope_name)

        if not scope_config:
            return False

        inspector = inspect(self)
        changed_fields = set()

        for field in scope_config.trigger_fields:
            if hasattr(inspector.attrs, field):
                history = getattr(inspector.attrs, field).history
                if history.has_changes():
                    changed_fields.add(field)

        return bool(changed_fields)

    def get_triggered_scopes(self) -> List[str]:
        """Get all scopes that should be triggered based on field changes"""
        scopes = self.__class__.get_webhook_scopes()
        return [scope_name for scope_name in scopes if self.is_webhook_triggered(scope_name)]

    def get_payload_for_scope(self, scope_name: str) -> PayloadType:
        """
        Get the payload for the specified scope based on its stage configuration.

        Returns:
            - For BOTH stage: Dict with 'before' and 'after' states
            - For BEFORE/AFTER stage: Dict with current state
        """
        scopes = self.__class__.get_webhook_scopes()
        if scope_name not in scopes:
            raise ValueError(f"Unknown scope: {scope_name}")

        scope_config = scopes[scope_name]
        fields_to_include = (
            set(scope_config.fields) if scope_config.fields else set(self.__table__.columns.keys())
        )

        if scope_config.stage == WebhookStage.BOTH:
            return {
                "before": self._get_payload_state(fields_to_include, state="before"),
                "after": self._get_payload_state(fields_to_include, state="after"),
            }

        state = "before" if scope_config.stage == WebhookStage.BEFORE else "after"
        return self._get_payload_state(fields_to_include, state)

    def _get_payload_state(
        self, fields: Set[str], state: Literal["before", "after"]
    ) -> Dict[str, Any]:
        """Get payload for specified fields in the requested state"""
        inspector = inspect(self)
        payload = {}

        for field in fields:
            if hasattr(inspector.attrs, field):
                history = getattr(inspector.attrs, field).history

                if state == "before":
                    value = history.deleted[0] if history.deleted else getattr(self, field)
                else:
                    value = history.added[0] if history.added else getattr(self, field)

                payload[field] = value

        return payload
