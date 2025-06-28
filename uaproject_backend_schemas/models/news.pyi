# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.file import File
from uaproject_backend_schemas.models.schemas.news import ImportanceType, NewsType
from uaproject_backend_schemas.models.user import User

class News(AwesomeModel):
    """Base news model."""

    author: Optional[User]
    author_id: int
    content: str
    created_at: datetime
    discord_message_id: Optional[str]
    event_time: Optional[datetime]
    id: int
    images: list[File]
    importance: ImportanceType
    is_archived: bool
    is_pinned: bool
    is_published: bool
    summary: Optional[str]
    tags: list[str]
    telegram_message_id: Optional[str]
    title: str
    type: NewsType
    updated_at: datetime
    schemas: NewsSchemas
    filter: type[NewsFilter]
    sort: type[NewsSort]

class NewsSchemas:
    """Schemas for the News model."""

    create: NewsSchemaCreate
    publish: NewsSchemaPublish
    redis: NewsSchemaRedis
    response: NewsSchemaResponse
    update: NewsSchemaUpdate
    update_meta: NewsSchemaUpdateMeta

class NewsSchemaCreate(AwesomeBaseModel):
    """create schema for News model"""

    event_time: Optional[datetime]
    importance: Optional[ImportanceType]
    tags: Optional[list[str]]
    discord_message_id: Optional[str]
    is_pinned: Optional[bool]
    telegram_message_id: Optional[str]
    is_archived: Optional[bool]
    title: Optional[str]
    type: Optional[NewsType]
    content: Optional[str]
    summary: Optional[str]

class NewsSchemaPublish(AwesomeBaseModel):
    """publish schema for News model"""

    id: Optional[int]
    is_published: Optional[bool]

class NewsSchemaRedis(AwesomeBaseModel):
    """redis schema for News model"""

    images: Optional[list[File]]
    author_id: Optional[int]
    event_time: Optional[datetime]
    importance: Optional[ImportanceType]
    tags: Optional[list[str]]
    discord_message_id: Optional[str]
    is_published: Optional[bool]
    author: Optional[User]
    updated_at: Optional[datetime]
    is_pinned: Optional[bool]
    telegram_message_id: Optional[str]
    is_archived: Optional[bool]
    title: Optional[str]
    type: Optional[NewsType]
    content: Optional[str]
    id: Optional[int]
    created_at: Optional[datetime]
    summary: Optional[str]

class NewsSchemaResponse(AwesomeBaseModel):
    """response schema for News model"""

    author_id: int
    event_time: Optional[datetime]
    importance: ImportanceType
    tags: list[str]
    discord_message_id: Optional[str]
    is_published: Optional[bool]
    updated_at: Optional[datetime]
    is_pinned: Optional[bool]
    telegram_message_id: Optional[str]
    is_archived: Optional[bool]
    title: str
    type: NewsType
    content: str
    id: Optional[int]
    created_at: Optional[datetime]
    summary: Optional[str]

class NewsSchemaUpdate(AwesomeBaseModel):
    """update schema for News model"""

    author_id: Optional[int]
    event_time: Optional[datetime]
    importance: Optional[ImportanceType]
    tags: Optional[list[str]]
    discord_message_id: Optional[str]
    is_published: Optional[bool]
    is_pinned: Optional[bool]
    telegram_message_id: Optional[str]
    is_archived: Optional[bool]
    title: Optional[str]
    type: Optional[NewsType]
    content: Optional[str]
    summary: Optional[str]

class NewsSchemaUpdateMeta(AwesomeBaseModel):
    """update_meta schema for News model"""

    id: Optional[int]
    is_pinned: Optional[bool]
    is_archived: Optional[bool]
    type: NewsType
    importance: ImportanceType

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

class NewsSort(StrEnum):
    """Enum for sorting the News model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
