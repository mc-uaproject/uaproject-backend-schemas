# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.types import SerializableHttpUrl
from uaproject_backend_schemas.models.schemas.webhook import WebhookStatus
from uaproject_backend_schemas.models.user import User

class Webhook(AwesomeModel):
    """Base webhook model."""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]
    created_at: datetime
    user: Optional[User]
    schemas: WebhookSchemas
    scopes: WebhookScopes
    filter: type[WebhookFilter]
    sort: type[WebhookSort]

class WebhookSchemas:
    """Schemas for the Webhook model."""

    create: WebhookSchemaCreate
    update: WebhookSchemaUpdate
    response: WebhookSchemaResponse

class WebhookSchemaCreate(AwesomeBaseModel):
    """create schema for Webhook model"""

    endpoint: Optional[SerializableHttpUrl]
    user_id: Optional[int]
    status: Optional[WebhookStatus]
    webhook_scopes: Optional[Dict]
    authorization: Optional[str]
    user: Optional[User]

class WebhookSchemaUpdate(AwesomeBaseModel):
    """update schema for Webhook model"""

    endpoint: Optional[SerializableHttpUrl]
    user_id: Optional[int]
    status: Optional[WebhookStatus]
    webhook_scopes: Optional[Dict]
    authorization: Optional[str]
    user: Optional[User]

class WebhookSchemaResponse(AwesomeBaseModel):
    """response schema for Webhook model"""

    updated_at: datetime
    id: int
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]
    user: Optional[User]

class WebhookScopes:
    """Scopes for the Webhook model."""

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
    authorization: Optional[str] = None

class WebhookSort(StrEnum):
    """Enum for sorting the Webhook model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
