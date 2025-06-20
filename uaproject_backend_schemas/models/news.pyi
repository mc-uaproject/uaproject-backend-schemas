# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.news_image import NewsImage
from uaproject_backend_schemas.models.schemas.news import ImportanceType, NewsType
from uaproject_backend_schemas.models.user import User

class News(AwesomeModel):
    """Base news model."""

    updated_at: datetime
    id: int
    title: str
    summary: Optional[str]
    content: str
    is_published: bool
    author_id: int
    discord_message_id: Optional[str]
    telegram_message_id: Optional[str]
    tags: List[str]
    event_time: Optional[datetime]
    is_pinned: bool
    is_archived: bool
    type: NewsType
    importance: ImportanceType
    created_at: datetime
    author: Optional[User]
    images: Optional[List[NewsImage]]
    cover_files: Optional[List[File]]
    schemas: NewsSchemas
    scopes: NewsScopes
    filter: type[NewsFilter]
    sort: type[NewsSort]

class NewsSchemas:
    """Schemas for the News model."""

    create: NewsSchemaCreate
    publish: NewsSchemaPublish
    update_meta: NewsSchemaUpdateMeta
    response: NewsSchemaResponse

class NewsSchemaCreate(AwesomeBaseModel):
    """create schema for News model"""

    title: str
    summary: Optional[str]
    content: str
    discord_message_id: Optional[str]
    telegram_message_id: Optional[str]
    tags: List[str]
    event_time: Optional[datetime]
    is_pinned: bool
    is_archived: bool
    type: NewsType
    importance: ImportanceType
    author: Optional[User]
    images: Optional[List[NewsImage]]
    cover_files: Optional[List[File]]

class NewsSchemaPublish(AwesomeBaseModel):
    """publish schema for News model"""

    is_published: bool

class NewsSchemaUpdateMeta(AwesomeBaseModel):
    """update_meta schema for News model"""

    is_pinned: bool
    is_archived: bool
    type: NewsType
    importance: ImportanceType

class NewsSchemaResponse(AwesomeBaseModel):
    """response schema for News model"""

    updated_at: datetime
    id: int
    title: str
    summary: Optional[str]
    content: str
    is_published: bool
    author_id: int
    discord_message_id: Optional[str]
    telegram_message_id: Optional[str]
    tags: List[str]
    event_time: Optional[datetime]
    is_pinned: bool
    is_archived: bool
    type: NewsType
    importance: ImportanceType
    author: Optional[User]
    images: Optional[List[NewsImage]]
    cover_files: Optional[List[File]]

class NewsScopes:
    """Scopes for the News model."""

class NewsFilter(BaseModel):
    """Pydantic-class for filtering the News model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    author_id: Optional[int] = None
    min_author_id: Optional[Any] = None
    max_author_id: Optional[Any] = None
    discord_message_id: Optional[str] = None
    telegram_message_id: Optional[str] = None
    event_time: Optional[datetime] = None
    min_event_time: Optional[Any] = None
    max_event_time: Optional[Any] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    type: Optional[NewsType] = None
    importance: Optional[ImportanceType] = None
    images_id: Optional[Any] = None
    cover_files_id: Optional[Any] = None

class NewsSort(StrEnum):
    """Enum for sorting the News model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
