# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.types import SerializableHttpUrl
from uaproject_backend_schemas.models.schemas.webhook import WebhookStatus
from uaproject_backend_schemas.models.user import User

class Webhook(AwesomeModel):
    """Base user model."""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]
    user: Optional[User]
    schemas: WebhookSchemas
    scopes: WebhookScopes
    filters: WebhookFilters
    filter: type[WebhookFilter]

class WebhookSchemas:
    """Schemas for the user model."""

    create: WebhookSchemaCreate
    update: WebhookSchemaUpdate
    response: WebhookSchemaResponse

class WebhookScopes:
    """Visibility scopes for the user model."""

    full: WebhookScopeFull

class WebhookFilters:
    """Declarative filters for the Webhook model."""

class WebhookFilter(BaseModel):
    """Pydantic-class for filtering the Webhook model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    endpoint: Optional[SerializableHttpUrl] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    status: Optional[WebhookStatus] = None
    webhook_scopes: Optional[Dict] = None
    authorization: Optional[str] = None

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
