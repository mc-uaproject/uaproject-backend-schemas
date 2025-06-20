# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.news import News
from uaproject_backend_schemas.models.service import Service
from uaproject_backend_schemas.models.ticket_message import TicketMessage
from uaproject_backend_schemas.models.user import User

class File(AwesomeModel):
    """Base file model."""

    updated_at: datetime
    id: int
    bucket: str
    path: str
    original_name: str
    content_type: str
    size: int
    checksum: Optional[str]
    checksum_type: str
    user_id: int
    model_name: Optional[str]
    model_id: Optional[int]
    status: str
    uploaded_at: Optional[datetime]
    ticket_message_id: Optional[int]
    news_id: Optional[int]
    service_id: Optional[int]
    created_at: datetime
    user: Optional[User]
    ticket_message: Optional[TicketMessage]
    news: Optional[News]
    service: Optional[Service]
    schemas: FileSchemas
    scopes: FileScopes
    filter: type[FileFilter]
    sort: type[FileSort]

class FileSchemas:
    """Schemas for the File model."""

    create: FileSchemaCreate
    update: FileSchemaUpdate
    response: FileSchemaResponse
    request_upload: FileSchemaRequestUpload

class FileSchemaCreate(AwesomeBaseModel):
    """create schema for File model"""

    bucket: str
    path: str
    original_name: str
    content_type: str
    size: int
    checksum: Optional[str]
    checksum_type: str
    user_id: int
    model_name: Optional[str]
    model_id: Optional[int]
    ticket_message_id: Optional[int]
    news_id: Optional[int]
    service_id: Optional[int]
    user: Optional[User]
    ticket_message: Optional[TicketMessage]
    news: Optional[News]
    service: Optional[Service]

class FileSchemaUpdate(AwesomeBaseModel):
    """update schema for File model"""

    status: str
    checksum: Optional[str]

class FileSchemaResponse(AwesomeBaseModel):
    """response schema for File model"""

    updated_at: datetime
    id: int
    bucket: str
    path: str
    original_name: str
    content_type: str
    size: int
    checksum: Optional[str]
    checksum_type: str
    user_id: int
    model_name: Optional[str]
    model_id: Optional[int]
    status: str
    uploaded_at: Optional[datetime]
    ticket_message_id: Optional[int]
    news_id: Optional[int]
    service_id: Optional[int]
    user: Optional[User]
    ticket_message: Optional[TicketMessage]
    news: Optional[News]
    service: Optional[Service]

class FileSchemaRequestUpload(AwesomeBaseModel):
    """request_upload schema for File model"""

    model_name: Optional[str]
    model_id: Optional[int]
    original_name: str
    content_type: str
    size: int

class FileScopes:
    """Scopes for the File model."""

    user_files: FileScopeUserFiles
    model_files: FileScopeModelFiles

class FileScopeUserFiles(AwesomeBaseModel):
    """user_files schema for File model"""

    id: int
    bucket: str
    path: str
    original_name: str
    content_type: str
    size: int
    status: str
    created_at: datetime

class FileScopeModelFiles(AwesomeBaseModel):
    """model_files schema for File model"""

    id: int
    bucket: str
    path: str
    original_name: str
    content_type: str
    size: int
    status: str
    created_at: datetime

class FileFilter(BaseModel):
    """Pydantic-class for filtering the File model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    bucket: Optional[str] = None
    path: Optional[str] = None
    original_name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    min_size: Optional[Any] = None
    max_size: Optional[Any] = None
    checksum: Optional[str] = None
    checksum_type: Optional[str] = None
    user_id: Optional[int] = None
    min_user_id: Optional[Any] = None
    max_user_id: Optional[Any] = None
    model_name: Optional[str] = None
    model_id: Optional[int] = None
    min_model_id: Optional[Any] = None
    max_model_id: Optional[Any] = None
    status: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    min_uploaded_at: Optional[Any] = None
    max_uploaded_at: Optional[Any] = None
    ticket_message_id: Optional[int] = None
    min_ticket_message_id: Optional[Any] = None
    max_ticket_message_id: Optional[Any] = None
    news_id: Optional[int] = None
    min_news_id: Optional[Any] = None
    max_news_id: Optional[Any] = None
    service_id: Optional[int] = None
    min_service_id: Optional[Any] = None
    max_service_id: Optional[Any] = None
    service_name: Optional[Any] = None

class FileSort(StrEnum):
    """Enum for sorting the File model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
