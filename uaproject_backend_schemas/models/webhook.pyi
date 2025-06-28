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
    created_at: datetime
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
    filter: type[WebhookFilter]
    sort: type[WebhookSort]

class WebhookSchemas:
    """Schemas for the Webhook model."""

    create: WebhookSchemaCreate
    redis: WebhookSchemaRedis
    response: WebhookSchemaResponse
    update: WebhookSchemaUpdate

class WebhookSchemaCreate(AwesomeBaseModel):
    """create schema for Webhook model"""

    triggers: Optional[list[WebhookTrigger]]
    user_id: Optional[int]
    endpoint: Optional[SerializableHttpUrl]
    schedule_timezone: Optional[str]
    priority: Optional[int]
    last_error_at: Optional[datetime]
    last_response_time_ms: Optional[int]
    auth_config: Optional[dict[str, Any]]
    last_triggered_at: Optional[datetime]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    last_success_at: Optional[datetime]
    auth_type: Optional[WebhookAuthType]
    average_response_time_ms: Optional[float]
    last_error: Optional[str]
    follow_redirects: Optional[bool]
    description: Optional[str]
    name: Optional[str]
    schedule_cron: Optional[str]
    status: Optional[WebhookStatus]
    verify_ssl: Optional[bool]
    success_triggers: Optional[int]
    failed_triggers: Optional[int]
    total_triggers: Optional[int]
    tags: Optional[list[str]]
    payload_config: Optional[WebhookPayloadTemplate]
    is_system: Optional[bool]
    retry_policy: Optional[WebhookRetryPolicy]
    last_response_status: Optional[int]

class WebhookSchemaRedis(AwesomeBaseModel):
    """redis schema for Webhook model"""

    triggers: Optional[list[WebhookTrigger]]
    user_id: Optional[int]
    endpoint: Optional[SerializableHttpUrl]
    user: Optional[User]
    schedule_timezone: Optional[str]
    logs: Optional[list[WebhookLog]]
    priority: Optional[int]
    last_error_at: Optional[datetime]
    last_response_time_ms: Optional[int]
    auth_config: Optional[dict[str, Any]]
    last_triggered_at: Optional[datetime]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    last_success_at: Optional[datetime]
    auth_type: Optional[WebhookAuthType]
    average_response_time_ms: Optional[float]
    last_error: Optional[str]
    updated_at: Optional[datetime]
    follow_redirects: Optional[bool]
    description: Optional[str]
    created_at: Optional[datetime]
    name: Optional[str]
    schedule_cron: Optional[str]
    status: Optional[WebhookStatus]
    verify_ssl: Optional[bool]
    success_triggers: Optional[int]
    failed_triggers: Optional[int]
    total_triggers: Optional[int]
    tags: Optional[list[str]]
    payload_config: Optional[WebhookPayloadTemplate]
    is_system: Optional[bool]
    retry_policy: Optional[WebhookRetryPolicy]
    id: Optional[int]
    last_response_status: Optional[int]

class WebhookSchemaResponse(AwesomeBaseModel):
    """response schema for Webhook model"""

    triggers: list[WebhookTrigger]
    user_id: Optional[int]
    endpoint: SerializableHttpUrl
    schedule_timezone: Optional[str]
    priority: Optional[int]
    last_error_at: Optional[datetime]
    last_response_time_ms: Optional[int]
    auth_config: Optional[dict[str, Any]]
    last_triggered_at: Optional[datetime]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    last_success_at: Optional[datetime]
    auth_type: Optional[WebhookAuthType]
    average_response_time_ms: Optional[float]
    last_error: Optional[str]
    updated_at: Optional[datetime]
    follow_redirects: Optional[bool]
    description: Optional[str]
    created_at: Optional[datetime]
    name: str
    schedule_cron: Optional[str]
    status: WebhookStatus
    verify_ssl: Optional[bool]
    success_triggers: Optional[int]
    failed_triggers: Optional[int]
    total_triggers: Optional[int]
    tags: Optional[list[str]]
    payload_config: WebhookPayloadTemplate
    is_system: Optional[bool]
    retry_policy: WebhookRetryPolicy
    id: Optional[int]
    last_response_status: Optional[int]

class WebhookSchemaUpdate(AwesomeBaseModel):
    """update schema for Webhook model"""

    triggers: Optional[list[WebhookTrigger]]
    user_id: Optional[int]
    endpoint: Optional[SerializableHttpUrl]
    schedule_timezone: Optional[str]
    priority: Optional[int]
    last_error_at: Optional[datetime]
    last_response_time_ms: Optional[int]
    auth_config: Optional[dict[str, Any]]
    last_triggered_at: Optional[datetime]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    last_success_at: Optional[datetime]
    auth_type: Optional[WebhookAuthType]
    average_response_time_ms: Optional[float]
    last_error: Optional[str]
    follow_redirects: Optional[bool]
    description: Optional[str]
    name: Optional[str]
    schedule_cron: Optional[str]
    status: Optional[WebhookStatus]
    verify_ssl: Optional[bool]
    success_triggers: Optional[int]
    failed_triggers: Optional[int]
    total_triggers: Optional[int]
    tags: Optional[list[str]]
    payload_config: Optional[WebhookPayloadTemplate]
    is_system: Optional[bool]
    retry_policy: Optional[WebhookRetryPolicy]
    last_response_status: Optional[int]

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
    logs_id: Optional[Any] = None

class WebhookSort(StrEnum):
    """Enum for sorting the Webhook model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
