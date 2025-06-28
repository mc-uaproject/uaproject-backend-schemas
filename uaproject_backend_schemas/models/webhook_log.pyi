# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.schemas.webhook import WebhookEvent, WebhookLogStatus
from uaproject_backend_schemas.models.webhook import Webhook

class WebhookLog(AwesomeModel):
    """Base webhooklog model."""

    attempt: int
    created_at: datetime
    event_id: UUID
    execution_duration_ms: Optional[int]
    id: int
    request_headers: dict[str, Any]
    request_payload: Optional[dict[str, Any]]
    request_payload_file: Optional[File]
    request_payload_file_id: Optional[int]
    response_body: Optional[str]
    response_body_file: Optional[File]
    response_body_file_id: Optional[int]
    response_headers: Optional[dict[str, Any]]
    response_status_code: Optional[int]
    status: WebhookLogStatus
    triggered_by_event: WebhookEvent
    updated_at: datetime
    webhook: Webhook
    webhook_id: int
    schemas: WebhookLogSchemas
    filter: type[WebhookLogFilter]
    sort: type[WebhookLogSort]

class WebhookLogSchemas:
    """Schemas for the WebhookLog model."""

    create: WebhookLogSchemaCreate
    redis: WebhookLogSchemaRedis
    response: WebhookLogSchemaResponse
    update: WebhookLogSchemaUpdate

class WebhookLogSchemaCreate(AwesomeBaseModel):
    """create schema for WebhookLog model"""

    status: Optional[WebhookLogStatus]
    event_id: Optional[UUID]
    execution_duration_ms: Optional[int]
    triggered_by_event: Optional[WebhookEvent]
    request_headers: Optional[dict[str, Any]]
    request_payload: Optional[dict[str, Any]]
    webhook_id: Optional[int]
    attempt: Optional[int]
    request_payload_file_id: Optional[int]
    response_body_file_id: Optional[int]
    response_status_code: Optional[int]
    response_body: Optional[str]
    response_headers: Optional[dict[str, Any]]

class WebhookLogSchemaRedis(AwesomeBaseModel):
    """redis schema for WebhookLog model"""

    webhook: Optional[Webhook]
    request_headers: Optional[dict[str, Any]]
    request_payload_file_id: Optional[int]
    execution_duration_ms: Optional[int]
    response_body_file: Optional[File]
    triggered_by_event: Optional[WebhookEvent]
    response_body_file_id: Optional[int]
    response_status_code: Optional[int]
    response_body: Optional[str]
    response_headers: Optional[dict[str, Any]]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    status: Optional[WebhookLogStatus]
    event_id: Optional[UUID]
    request_payload_file: Optional[File]
    request_payload: Optional[dict[str, Any]]
    webhook_id: Optional[int]
    attempt: Optional[int]
    id: Optional[int]

class WebhookLogSchemaResponse(AwesomeBaseModel):
    """response schema for WebhookLog model"""

    status: WebhookLogStatus
    event_id: Optional[UUID]
    execution_duration_ms: Optional[int]
    triggered_by_event: WebhookEvent
    request_headers: dict[str, Any]
    request_payload: Optional[dict[str, Any]]
    webhook_id: int
    updated_at: Optional[datetime]
    attempt: Optional[int]
    request_payload_file_id: Optional[int]
    response_body_file_id: Optional[int]
    response_status_code: Optional[int]
    created_at: Optional[datetime]
    response_body: Optional[str]
    id: Optional[int]
    response_headers: Optional[dict[str, Any]]

class WebhookLogSchemaUpdate(AwesomeBaseModel):
    """update schema for WebhookLog model"""

    status: Optional[WebhookLogStatus]
    event_id: Optional[UUID]
    execution_duration_ms: Optional[int]
    triggered_by_event: Optional[WebhookEvent]
    request_headers: Optional[dict[str, Any]]
    request_payload: Optional[dict[str, Any]]
    webhook_id: Optional[int]
    attempt: Optional[int]
    request_payload_file_id: Optional[int]
    response_body_file_id: Optional[int]
    response_status_code: Optional[int]
    response_body: Optional[str]
    response_headers: Optional[dict[str, Any]]

class WebhookLogFilter(BaseModel):
    """Pydantic-class for filtering the WebhookLog model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    event_id: Optional[UUID] = None
    webhook_id: Optional[int] = None
    min_webhook_id: Optional[Any] = None
    max_webhook_id: Optional[Any] = None
    status: Optional[WebhookLogStatus] = None
    triggered_by_event: Optional[WebhookEvent] = None
    attempt: Optional[int] = None
    min_attempt: Optional[Any] = None
    max_attempt: Optional[Any] = None
    request_payload_file_id: Optional[int] = None
    min_request_payload_file_id: Optional[Any] = None
    max_request_payload_file_id: Optional[Any] = None
    response_status_code: Optional[int] = None
    min_response_status_code: Optional[Any] = None
    max_response_status_code: Optional[Any] = None
    response_body: Optional[str] = None
    response_body_file_id: Optional[int] = None
    min_response_body_file_id: Optional[Any] = None
    max_response_body_file_id: Optional[Any] = None
    execution_duration_ms: Optional[int] = None
    min_execution_duration_ms: Optional[Any] = None
    max_execution_duration_ms: Optional[Any] = None
    webhook_name: Optional[Any] = None

class WebhookLogSort(StrEnum):
    """Enum for sorting the WebhookLog model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
