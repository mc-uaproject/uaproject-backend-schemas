from typing import Dict, Optional, Set

from pydantic import BaseModel

from uaproject_backend_schemas.webhooks.mixins.config import (
    ActionConfigModel,
    RelationshipConfigModel,
    TemporalFieldConfig,
)
from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["WebhookScopeFields", "WebhookBaseMixin"]


class WebhookScopeFields(BaseModel):
    """Configuration for webhook scope fields"""

    trigger_fields: list[str]
    fields: Optional[list[str]] = None
    stage: WebhookStage = WebhookStage.AFTER
    relationships: Optional[Dict[str, RelationshipConfigModel]] = None
    temporal_fields: Optional[list[TemporalFieldConfig]] = None
    actions: Optional[list[ActionConfigModel]] = None


class WebhookBaseMixin:
    """Base mixin for webhook functionality"""

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
        trigger_fields: list[str] | Set[str],
        fields: list[str] | Set[str] | BaseModel | None = None,
        relationships: Optional[Dict[str, RelationshipConfigModel]] | None = None,
        stage: WebhookStage = WebhookStage.AFTER,
        temporal_fields: Optional[list[TemporalFieldConfig]] | None = None,
        actions: Optional[list[ActionConfigModel]] = None,
    ) -> None:
        """
        Register a new scope for the model with specified
        trigger fields, optional payload fields and relationships.

        Args:
            scope_name: Unique identifier for the scope
            trigger_fields: Fields that will trigger the webhook when modified
            fields: Optional specific fields to include in the payload.
                   If None, all fields will be included. Can also be a Pydantic BaseModel.
            relationships: Optional dictionary mapping relationship names to their configurations
            stage: WebhookStage indicating when the webhook should be triggered
            temporal_fields: Optional list of temporal field configurations
            actions: Optional list of action configurations
        """

        scope_name = f"{cls.__scope_prefix__}.{scope_name}"
        scopes = cls.get_webhook_scopes()

        if scope_name in scopes:
            raise ValueError(f"Scope '{scope_name}' is already registered for {cls.__name__}")

        trigger_fields_set = set(trigger_fields)
        fields_set = cls._process_fields(fields)

        cls._validate_trigger_fields(trigger_fields_set)
        cls._validate_payload_fields(fields_set, relationships)

        if not any(base.__name__ == "WebhookChangesMixin" for base in cls.__bases__):
            raise TypeError(
                f"Class {cls.__name__} must inherit from WebhookChangesMixin to use webhooks"
            )

        if relationships:
            if not any(base.__name__ == "WebhookRelationshipsMixin" for base in cls.__bases__):
                raise TypeError(
                    f"Class {cls.__name__} must inherit from WebhookRelationshipsMixin to use relationships"
                )

            relationship_configs = cls._process_relationships(relationships)

        if temporal_fields:
            if not any(base.__name__ == "WebhookTemporalMixin" for base in cls.__bases__):
                raise TypeError(
                    f"Class {cls.__name__} must inherit from WebhookTemporalMixin to use temporal fields"
                )

            temporal_field_configs = cls._process_temporal_fields(temporal_fields)

        if actions:
            if not any(base.__name__ == "WebhookActionsMixin" for base in cls.__bases__):
                raise TypeError(
                    f"Class {cls.__name__} must inherit from WebhookActionsMixin to use actions"
                )

            action_configs = cls._process_actions(actions)

        scopes[scope_name] = WebhookScopeFields(
            trigger_fields=list(trigger_fields_set),
            fields=list(fields_set) if fields_set else None,
            relationships=relationship_configs,
            stage=stage,
            temporal_fields=temporal_field_configs,
            actions=action_configs,
        )
