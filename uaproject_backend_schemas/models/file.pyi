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

    access_level: str
    bucket: str
    created_at: datetime
    id: int
    is_public: bool
    model_id: Optional[int]
    model_name: Optional[str]
    news: Optional[News]
    news_id: Optional[int]
    path: str
    service: Optional[Service]
    service_id: Optional[int]
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

    service_id: Optional[int]
    bucket: Optional[str]
    news_id: Optional[int]
    model_name: Optional[str]
    status: Optional[str]
    ticket_message_id: Optional[int]
    user_id: Optional[int]
    model_id: Optional[int]
    is_public: Optional[bool]
    access_level: Optional[str]
    path: Optional[str]

class FileSchemaRedis(AwesomeBaseModel):
    """redis schema for File model"""

    service_id: Optional[int]
    user: Optional[User]
    model_name: Optional[str]
    ticket_message_id: Optional[int]
    ticket_message: Optional[TicketMessage]
    is_public: Optional[bool]
    path: Optional[str]
    webhook_logs_as_response: Optional[list[WebhookLog]]
    news: Optional[News]
    status: Optional[str]
    user_id: Optional[int]
    updated_at: Optional[datetime]
    bucket: Optional[str]
    news_id: Optional[int]
    model_id: Optional[int]
    access_level: Optional[str]
    id: Optional[int]
    webhook_logs_as_request: Optional[list[WebhookLog]]
    service: Optional[Service]
    uploaded_at: Optional[datetime]
    created_at: datetime

class FileSchemaRequestUpload(AwesomeBaseModel):
    """request_upload schema for File model"""

    id: Optional[int]
    model_name: Optional[str]
    model_id: Optional[int]
    is_public: Optional[bool]
    created_at: datetime

class FileSchemaResponse(AwesomeBaseModel):
    """response schema for File model"""

    service_id: Optional[int]
    bucket: str
    news_id: Optional[int]
    model_name: Optional[str]
    status: str
    ticket_message_id: Optional[int]
    user_id: int
    model_id: Optional[int]
    is_public: Optional[bool]
    access_level: str
    path: str
    id: Optional[int]
    updated_at: Optional[datetime]
    uploaded_at: Optional[datetime]
    created_at: datetime

class FileSchemaUpdate(AwesomeBaseModel):
    """update schema for File model"""

    id: Optional[int]
    status: Optional[str]
    is_public: Optional[bool]
    access_level: Optional[str]
    created_at: datetime

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
    user_id: Optional[int] = None
    min_user_id: Optional[int] = None
    max_user_id: Optional[int] = None
    model_name: Optional[str] = None
    model_id: Optional[int] = None
    min_model_id: Optional[int] = None
    max_model_id: Optional[int] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    access_level: Optional[str] = None
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
