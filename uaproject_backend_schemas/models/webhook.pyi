# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.types import SerializableHttpUrl
from uaproject_backend_schemas.models.schemas.webhook import (
    WebhookAuthType,
    WebhookPayloadTemplate,
    WebhookRetryPolicy,
    WebhookStatus,
    WebhookTrigger,
)
from uaproject_backend_schemas.models.user import User
from uaproject_backend_schemas.models.webhook_log import WebhookLog

class Webhook(AwesomeModel):
    """Base webhook model."""

    auth_config: Optional[dict[str, Any]]
    auth_type: Optional[WebhookAuthType]
    average_response_time_ms: Optional[float]
    description: Optional[str]
    endpoint: SerializableHttpUrl
    failed_triggers: int
    follow_redirects: bool
    id: int
    is_system: bool
    last_error: Optional[str]
    last_error_at: Optional[datetime]
    last_response_status: Optional[int]
    last_response_time_ms: Optional[int]
    last_success_at: Optional[datetime]
    last_triggered_at: Optional[datetime]
    logs: list[WebhookLog]
    name: str
    payload_config: WebhookPayloadTemplate
    priority: int
    retry_policy: WebhookRetryPolicy
    schedule_cron: Optional[str]
    schedule_timezone: Optional[str]
    status: WebhookStatus
    success_triggers: int
    tags: Optional[list[str]]
    timeout: int
    total_triggers: int
    triggers: list[WebhookTrigger]
    updated_at: datetime
    user: Optional[User]
    user_id: Optional[int]
    verify_ssl: bool
    webhook_metadata: Optional[dict[str, Any]]
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

    name: Optional[str]
    description: Optional[str]
    endpoint: Optional[SerializableHttpUrl]
    user_id: Optional[int]
    status: Optional[WebhookStatus]
    is_system: Optional[bool]
    priority: Optional[int]
    triggers: Optional[list[WebhookTrigger]]
    payload_config: Optional[WebhookPayloadTemplate]
    retry_policy: Optional[WebhookRetryPolicy]
    auth_type: Optional[WebhookAuthType]
    auth_config: Optional[dict[str, Any]]
    timeout: Optional[int]
    follow_redirects: Optional[bool]
    verify_ssl: Optional[bool]
    schedule_cron: Optional[str]
    schedule_timezone: Optional[str]
    last_triggered_at: Optional[datetime]
    last_success_at: Optional[datetime]
    last_error: Optional[str]
    last_error_at: Optional[datetime]
    last_response_status: Optional[int]
    last_response_time_ms: Optional[int]
    total_triggers: Optional[int]
    success_triggers: Optional[int]
    failed_triggers: Optional[int]
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    webhook_metadata: Optional[dict[str, Any]]
    user: Optional[User]
    logs: Optional[list[WebhookLog]]

class WebhookSchemaUpdate(AwesomeBaseModel):
    """update schema for Webhook model"""

    name: Optional[str]
    description: Optional[str]
    endpoint: Optional[SerializableHttpUrl]
    user_id: Optional[int]
    status: Optional[WebhookStatus]
    is_system: Optional[bool]
    priority: Optional[int]
    triggers: Optional[list[WebhookTrigger]]
    payload_config: Optional[WebhookPayloadTemplate]
    retry_policy: Optional[WebhookRetryPolicy]
    auth_type: Optional[WebhookAuthType]
    auth_config: Optional[dict[str, Any]]
    timeout: Optional[int]
    follow_redirects: Optional[bool]
    verify_ssl: Optional[bool]
    schedule_cron: Optional[str]
    schedule_timezone: Optional[str]
    last_triggered_at: Optional[datetime]
    last_success_at: Optional[datetime]
    last_error: Optional[str]
    last_error_at: Optional[datetime]
    last_response_status: Optional[int]
    last_response_time_ms: Optional[int]
    total_triggers: Optional[int]
    success_triggers: Optional[int]
    failed_triggers: Optional[int]
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    webhook_metadata: Optional[dict[str, Any]]
    user: Optional[User]
    logs: Optional[list[WebhookLog]]

class WebhookSchemaResponse(AwesomeBaseModel):
    """response schema for Webhook model"""

    updated_at: datetime
    id: int
    name: str
    description: Optional[str]
    endpoint: SerializableHttpUrl
    user_id: Optional[int]
    status: WebhookStatus
    is_system: bool
    priority: int
    triggers: list[WebhookTrigger]
    payload_config: WebhookPayloadTemplate
    retry_policy: WebhookRetryPolicy
    auth_type: Optional[WebhookAuthType]
    auth_config: Optional[dict[str, Any]]
    timeout: int
    follow_redirects: bool
    verify_ssl: bool
    schedule_cron: Optional[str]
    schedule_timezone: Optional[str]
    last_triggered_at: Optional[datetime]
    last_success_at: Optional[datetime]
    last_error: Optional[str]
    last_error_at: Optional[datetime]
    last_response_status: Optional[int]
    last_response_time_ms: Optional[int]
    total_triggers: int
    success_triggers: int
    failed_triggers: int
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    webhook_metadata: Optional[dict[str, Any]]
    user: Optional[User]
    logs: list[WebhookLog]

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
    name: Optional[str] = None
    description: Optional[str] = None
    endpoint: Optional[SerializableHttpUrl] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    status: Optional[WebhookStatus] = None
    is_system: Optional[bool] = None
    priority: Optional[int] = None
    min_priority: Optional[Any] = None
    max_priority: Optional[Any] = None
    payload_config: Optional[WebhookPayloadTemplate] = None
    retry_policy: Optional[WebhookRetryPolicy] = None
    auth_type: Optional[WebhookAuthType] = None
    timeout: Optional[int] = None
    min_timeout: Optional[Any] = None
    max_timeout: Optional[Any] = None
    follow_redirects: Optional[bool] = None
    verify_ssl: Optional[bool] = None
    schedule_cron: Optional[str] = None
    schedule_timezone: Optional[str] = None
    last_triggered_at: Optional[datetime] = None
    min_last_triggered_at: Optional[Any] = None
    max_last_triggered_at: Optional[Any] = None
    last_success_at: Optional[datetime] = None
    min_last_success_at: Optional[Any] = None
    max_last_success_at: Optional[Any] = None
    last_error: Optional[str] = None
    last_error_at: Optional[datetime] = None
    min_last_error_at: Optional[Any] = None
    max_last_error_at: Optional[Any] = None
    last_response_status: Optional[int] = None
    min_last_response_status: Optional[Any] = None
    max_last_response_status: Optional[Any] = None
    last_response_time_ms: Optional[int] = None
    min_last_response_time_ms: Optional[Any] = None
    max_last_response_time_ms: Optional[Any] = None
    total_triggers: Optional[int] = None
    min_total_triggers: Optional[Any] = None
    max_total_triggers: Optional[Any] = None
    success_triggers: Optional[int] = None
    min_success_triggers: Optional[Any] = None
    max_success_triggers: Optional[Any] = None
    failed_triggers: Optional[int] = None
    min_failed_triggers: Optional[Any] = None
    max_failed_triggers: Optional[Any] = None
    average_response_time_ms: Optional[float] = None
    min_average_response_time_ms: Optional[Any] = None
    max_average_response_time_ms: Optional[Any] = None

class WebhookSort(StrEnum):
    """Enum for sorting the Webhook model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
