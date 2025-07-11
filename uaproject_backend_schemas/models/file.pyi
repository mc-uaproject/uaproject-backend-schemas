# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.news import News
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.ticket_message import TicketMessage
from uaproject_backend_schemas.models.user import User
from uaproject_backend_schemas.models.webhook_log import WebhookLog

class File(AwesomeModel):
    """Base file model."""

    bucket: str
    checksum: Optional[str]
    checksum_type: str
    content_type: str
    created_at: datetime
    id: int
    model_id: Optional[int]
    model_name: Optional[str]
    news: Optional[News]
    news_id: Optional[int]
    original_name: str
    path: str
    service: Optional[Service]
    service_id: Optional[int]
    size: int
    status: str
    ticket_message: Optional[TicketMessage]
    ticket_message_id: Optional[int]
    updated_at: datetime
    uploaded_at: Optional[datetime]
    user: Optional[User]
    user_id: int
    webhook_logs_as_request: list[WebhookLog]
    webhook_logs_as_response: list[WebhookLog]
    schemas: FileSchemas
    filter: type[FileFilter]
    sort: type[FileSort]

class FileSchemas:
    """Schemas for the File model."""

    create: FileSchemaCreate
    redis: FileSchemaRedis
    request_upload: FileSchemaRequestUpload
    response: FileSchemaResponse
    update: FileSchemaUpdate

class FileSchemaCreate(AwesomeBaseModel):
    """create schema for File model"""

    checksum: Optional[str]
    user_id: Optional[int]
    news_id: Optional[int]
    model_id: Optional[int]
    size: Optional[int]
    checksum_type: Optional[str]
    model_name: Optional[str]
    content_type: Optional[str]
    bucket: Optional[str]
    original_name: Optional[str]
    service_id: Optional[int]
    ticket_message_id: Optional[int]
    path: Optional[str]

class FileSchemaRedis(AwesomeBaseModel):
    """redis schema for File model"""

    checksum: Optional[str]
    ticket_message: Optional[TicketMessage]
    user_id: Optional[int]
    size: Optional[int]
    uploaded_at: Optional[datetime]
    user: Optional[User]
    service_id: Optional[int]
    status: Optional[str]
    path: Optional[str]
    model_id: Optional[int]
    service: Optional[Service]
    updated_at: Optional[datetime]
    ticket_message_id: Optional[int]
    news_id: Optional[int]
    webhook_logs_as_request: Optional[list[WebhookLog]]
    checksum_type: Optional[str]
    model_name: Optional[str]
    webhook_logs_as_response: Optional[list[WebhookLog]]
    content_type: Optional[str]
    bucket: Optional[str]
    original_name: Optional[str]
    news: Optional[News]
    id: Optional[int]
    created_at: datetime

class FileSchemaRequestUpload(AwesomeBaseModel):
    """request_upload schema for File model"""

    id: Optional[int]
    model_name: Optional[str]
    model_id: Optional[int]
    original_name: str
    content_type: str
    size: int

class FileSchemaResponse(AwesomeBaseModel):
    """response schema for File model"""

    checksum: Optional[str]
    user_id: int
    news_id: Optional[int]
    model_id: Optional[int]
    size: int
    checksum_type: Optional[str]
    model_name: Optional[str]
    content_type: str
    uploaded_at: Optional[datetime]
    bucket: str
    original_name: str
    updated_at: Optional[datetime]
    service_id: Optional[int]
    ticket_message_id: Optional[int]
    id: Optional[int]
    status: str
    path: str
    created_at: datetime

class FileSchemaUpdate(AwesomeBaseModel):
    """update schema for File model"""

    id: Optional[int]
    status: Optional[str]
    checksum: Optional[str]

class FileFilter(BaseModel):
    """Pydantic-class for filtering the File model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    bucket: Optional[str] = None
    path: Optional[str] = None
    original_name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    checksum: Optional[str] = None
    checksum_type: Optional[str] = None
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    model_name: Optional[str] = None
    model_id: Optional[int] = None
    min_model_id: Optional[int] = None
    max_model_id: Optional[int] = None
    status: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    min_uploaded_at: Optional[datetime] = None
    max_uploaded_at: Optional[datetime] = None
    ticket_message_id: Optional[int] = None
    min_ticket_message_id: Optional[int] = None
    max_ticket_message_id: Optional[int] = None
    news_id: Optional[int] = None
    min_news_id: Optional[int] = None
    max_news_id: Optional[int] = None
    service_id: Optional[int] = None
    min_service_id: Optional[int] = None
    max_service_id: Optional[int] = None
    service_name: Optional[str] = None
    webhook_logs_as_request_id: Optional[int] = None
    webhook_logs_as_response_id: Optional[int] = None

class FileSort(StrEnum):
    """Enum for sorting the File model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
