from enum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class WebhookStatus(StrEnum):
    ACTIVE = "active"
    UNRESPONSIVE = "unresponsive"
    PROCESSING = "processing"
    ERROR = "error"


class WebhookTriggerFields(BaseModel):
    """Configuration for webhook trigger fields per model"""

    model_name: str = Field(description="Name of the model to watch")
    fields: List[str] = Field(description="List of field names to watch for changes")
    events: List[str] = Field(
        default=["create", "update", "delete"], description="Events to trigger on"
    )


class WebhookScopeConfig(BaseModel):
    """Dynamic webhook scope configuration"""

    enabled: bool = Field(default=True, description="Whether this scope is enabled")
    trigger_fields: List[WebhookTriggerFields] = Field(
        default_factory=list, description="Field configurations for different models"
    )
    filters: Optional[Dict[str, any]] = Field(
        default=None, description="Additional filters for this scope"
    )
