# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Dict, Optional

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
    filters: WebhookFilters
    sorts: WebhookSorts
    filter: type[WebhookFilter]
    sort: type[WebhookSort]

class WebhookSchemas:
    """Schemas for the Webhook model."""

    create: WebhookSchemaCreate
    update: WebhookSchemaUpdate
    response: WebhookSchemaResponse

class WebhookSchemaCreate(AwesomeBaseModel):
    """create schema for Webhook model"""

    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
    authorization: Optional[str]
    user: Optional[User]

class WebhookSchemaUpdate(AwesomeBaseModel):
    """update schema for Webhook model"""

    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    webhook_scopes: Dict
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

class WebhookFilters:
    """Declarative filters for the Webhook model."""

class WebhookFilter(BaseModel):
    """Pydantic-class for filtering the Webhook model."""

class WebhookSorts:
    """Declarative sorts for the Webhook model."""

class WebhookSort(StrEnum):
    """Enum for sorting the Webhook model."""
