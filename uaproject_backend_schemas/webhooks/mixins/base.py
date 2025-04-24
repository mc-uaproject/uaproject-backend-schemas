from typing import Dict, Optional

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
