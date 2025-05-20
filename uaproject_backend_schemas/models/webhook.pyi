# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Dict, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.types import SerializableHttpUrl
from uaproject_backend_schemas.models.schemas.webhook import WebhookStatus

class Webhook(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]
    schemas: WebhookSchemas
    scopes: WebhookScopes

class WebhookSchemas:
    """Schemas for the user model."""

    create: WebhookSchemaCreate
    update: WebhookSchemaUpdate
    response: WebhookSchemaResponse

class WebhookScopes:
    """Visibility scopes for the user model."""

    full: WebhookScopeFull

class WebhookSchemaCreate(AwesomeBaseModel):
    """Create schema for Webhook model"""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]

class WebhookSchemaUpdate(AwesomeBaseModel):
    """Update schema for Webhook model"""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]

class WebhookSchemaResponse(AwesomeBaseModel):
    """Response schema for Webhook model"""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]

class WebhookScopeFull(AwesomeBaseModel):
    """full visibility scope for Webhook model"""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]
