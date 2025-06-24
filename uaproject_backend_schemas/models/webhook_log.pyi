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
    scopes: WebhookLogScopes
    filter: type[WebhookLogFilter]
    sort: type[WebhookLogSort]

class WebhookLogSchemas:
    """Schemas for the WebhookLog model."""

    create: WebhookLogSchemaCreate
    update: WebhookLogSchemaUpdate
    response: WebhookLogSchemaResponse

class WebhookLogSchemaCreate(AwesomeBaseModel):
    """create schema for WebhookLog model"""

    event_id: Optional[UUID]
    webhook_id: Optional[int]
    status: Optional[WebhookLogStatus]
    triggered_by_event: Optional[WebhookEvent]
    attempt: Optional[int]
    request_headers: Optional[dict[str, Any]]
    request_payload: Optional[dict[str, Any]]
    request_payload_file_id: Optional[int]
    response_status_code: Optional[int]
    response_headers: Optional[dict[str, Any]]
    response_body: Optional[str]
    response_body_file_id: Optional[int]
    execution_duration_ms: Optional[int]
    webhook: Optional[Webhook]
    request_payload_file: Optional[File]
    response_body_file: Optional[File]

class WebhookLogSchemaUpdate(AwesomeBaseModel):
    """update schema for WebhookLog model"""

    event_id: Optional[UUID]
    webhook_id: Optional[int]
    status: Optional[WebhookLogStatus]
    triggered_by_event: Optional[WebhookEvent]
    attempt: Optional[int]
    request_headers: Optional[dict[str, Any]]
    request_payload: Optional[dict[str, Any]]
    request_payload_file_id: Optional[int]
    response_status_code: Optional[int]
    response_headers: Optional[dict[str, Any]]
    response_body: Optional[str]
    response_body_file_id: Optional[int]
    execution_duration_ms: Optional[int]
    webhook: Optional[Webhook]
    request_payload_file: Optional[File]
    response_body_file: Optional[File]

class WebhookLogSchemaResponse(AwesomeBaseModel):
    """response schema for WebhookLog model"""

    updated_at: datetime
    id: int
    event_id: UUID
    webhook_id: int
    status: WebhookLogStatus
    triggered_by_event: WebhookEvent
    attempt: int
    request_headers: dict[str, Any]
    request_payload: Optional[dict[str, Any]]
    request_payload_file_id: Optional[int]
    response_status_code: Optional[int]
    response_headers: Optional[dict[str, Any]]
    response_body: Optional[str]
    response_body_file_id: Optional[int]
    execution_duration_ms: Optional[int]
    webhook: Webhook
    request_payload_file: Optional[File]
    response_body_file: Optional[File]

class WebhookLogScopes:
    """Scopes for the WebhookLog model."""

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
