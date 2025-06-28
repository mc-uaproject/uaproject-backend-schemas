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

    last_triggered_at: Optional[datetime]
    payload_config: Optional[WebhookPayloadTemplate]
    total_triggers: Optional[int]
    failed_triggers: Optional[int]
    priority: Optional[int]
    schedule_cron: Optional[str]
    last_response_status: Optional[int]
    verify_ssl: Optional[bool]
    is_system: Optional[bool]
    last_success_at: Optional[datetime]
    auth_config: Optional[dict[str, Any]]
    user_id: Optional[int]
    schedule_timezone: Optional[str]
    success_triggers: Optional[int]
    last_error: Optional[str]
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    retry_policy: Optional[WebhookRetryPolicy]
    description: Optional[str]
    status: Optional[WebhookStatus]
    last_error_at: Optional[datetime]
    endpoint: Optional[SerializableHttpUrl]
    last_response_time_ms: Optional[int]
    triggers: Optional[list[WebhookTrigger]]
    follow_redirects: Optional[bool]
    auth_type: Optional[WebhookAuthType]
    name: Optional[str]

class WebhookSchemaRedis(AwesomeBaseModel):
    """redis schema for Webhook model"""

    last_triggered_at: Optional[datetime]
    payload_config: Optional[WebhookPayloadTemplate]
    logs: Optional[list[WebhookLog]]
    created_at: Optional[datetime]
    total_triggers: Optional[int]
    failed_triggers: Optional[int]
    user: Optional[User]
    priority: Optional[int]
    schedule_cron: Optional[str]
    last_response_status: Optional[int]
    verify_ssl: Optional[bool]
    is_system: Optional[bool]
    last_success_at: Optional[datetime]
    auth_config: Optional[dict[str, Any]]
    user_id: Optional[int]
    schedule_timezone: Optional[str]
    success_triggers: Optional[int]
    last_error: Optional[str]
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    updated_at: Optional[datetime]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    retry_policy: Optional[WebhookRetryPolicy]
    description: Optional[str]
    id: Optional[int]
    status: Optional[WebhookStatus]
    last_error_at: Optional[datetime]
    endpoint: Optional[SerializableHttpUrl]
    last_response_time_ms: Optional[int]
    triggers: Optional[list[WebhookTrigger]]
    follow_redirects: Optional[bool]
    auth_type: Optional[WebhookAuthType]
    name: Optional[str]

class WebhookSchemaResponse(AwesomeBaseModel):
    """response schema for Webhook model"""

    last_triggered_at: Optional[datetime]
    payload_config: WebhookPayloadTemplate
    created_at: Optional[datetime]
    total_triggers: Optional[int]
    failed_triggers: Optional[int]
    priority: Optional[int]
    schedule_cron: Optional[str]
    last_response_status: Optional[int]
    verify_ssl: Optional[bool]
    is_system: Optional[bool]
    last_success_at: Optional[datetime]
    auth_config: Optional[dict[str, Any]]
    user_id: Optional[int]
    schedule_timezone: Optional[str]
    success_triggers: Optional[int]
    last_error: Optional[str]
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    updated_at: Optional[datetime]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    retry_policy: WebhookRetryPolicy
    description: Optional[str]
    id: Optional[int]
    status: WebhookStatus
    last_error_at: Optional[datetime]
    endpoint: SerializableHttpUrl
    last_response_time_ms: Optional[int]
    triggers: list[WebhookTrigger]
    follow_redirects: Optional[bool]
    auth_type: Optional[WebhookAuthType]
    name: str

class WebhookSchemaUpdate(AwesomeBaseModel):
    """update schema for Webhook model"""

    last_triggered_at: Optional[datetime]
    payload_config: Optional[WebhookPayloadTemplate]
    total_triggers: Optional[int]
    failed_triggers: Optional[int]
    priority: Optional[int]
    schedule_cron: Optional[str]
    last_response_status: Optional[int]
    verify_ssl: Optional[bool]
    is_system: Optional[bool]
    last_success_at: Optional[datetime]
    auth_config: Optional[dict[str, Any]]
    user_id: Optional[int]
    schedule_timezone: Optional[str]
    success_triggers: Optional[int]
    last_error: Optional[str]
    average_response_time_ms: Optional[float]
    tags: Optional[list[str]]
    timeout: Optional[int]
    webhook_metadata: Optional[dict[str, Any]]
    retry_policy: Optional[WebhookRetryPolicy]
    description: Optional[str]
    status: Optional[WebhookStatus]
    last_error_at: Optional[datetime]
    endpoint: Optional[SerializableHttpUrl]
    last_response_time_ms: Optional[int]
    triggers: Optional[list[WebhookTrigger]]
    follow_redirects: Optional[bool]
    auth_type: Optional[WebhookAuthType]
    name: Optional[str]

class WebhookFilter(BaseModel):
    """Pydantic-class for filtering the Webhook model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    endpoint: Optional[SerializableHttpUrl] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    status: Optional[WebhookStatus] = None
    is_system: Optional[bool] = None
    priority: Optional[int] = None
    min_priority: Optional[int] = None
    max_priority: Optional[int] = None
    payload_config: Optional[WebhookPayloadTemplate] = None
    retry_policy: Optional[WebhookRetryPolicy] = None
    auth_type: Optional[WebhookAuthType] = None
    timeout: Optional[int] = None
    min_timeout: Optional[int] = None
    max_timeout: Optional[int] = None
    follow_redirects: Optional[bool] = None
    verify_ssl: Optional[bool] = None
    schedule_cron: Optional[str] = None
    schedule_timezone: Optional[str] = None
    last_triggered_at: Optional[datetime] = None
    min_last_triggered_at: Optional[datetime] = None
    max_last_triggered_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    min_last_success_at: Optional[datetime] = None
    max_last_success_at: Optional[datetime] = None
    last_error: Optional[str] = None
    last_error_at: Optional[datetime] = None
    min_last_error_at: Optional[datetime] = None
    max_last_error_at: Optional[datetime] = None
    last_response_status: Optional[int] = None
    min_last_response_status: Optional[int] = None
    max_last_response_status: Optional[int] = None
    last_response_time_ms: Optional[int] = None
    min_last_response_time_ms: Optional[int] = None
    max_last_response_time_ms: Optional[int] = None
    total_triggers: Optional[int] = None
    min_total_triggers: Optional[int] = None
    max_total_triggers: Optional[int] = None
    success_triggers: Optional[int] = None
    min_success_triggers: Optional[int] = None
    max_success_triggers: Optional[int] = None
    failed_triggers: Optional[int] = None
    min_failed_triggers: Optional[int] = None
    max_failed_triggers: Optional[int] = None
    average_response_time_ms: Optional[float] = None
    min_average_response_time_ms: Optional[float] = None
    max_average_response_time_ms: Optional[float] = None
    logs_id: Optional[int] = None

class WebhookSort(StrEnum):
    """Enum for sorting the Webhook model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
