# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

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

    type: Optional[NewsType]
    is_pinned: Optional[bool]
    tags: Optional[list[str]]
    is_archived: Optional[bool]
    summary: Optional[str]
    event_time: Optional[datetime]
    discord_message_id: Optional[str]
    title: Optional[str]
    telegram_message_id: Optional[str]
    importance: Optional[ImportanceType]
    content: Optional[str]

class NewsSchemaPublish(AwesomeBaseModel):
    """publish schema for News model"""

    id: Optional[int]
    is_published: Optional[bool]

class NewsSchemaRedis(AwesomeBaseModel):
    """redis schema for News model"""

    type: Optional[NewsType]
    is_pinned: Optional[bool]
    tags: Optional[list[str]]
    is_archived: Optional[bool]
    id: Optional[int]
    summary: Optional[str]
    author_id: Optional[int]
    event_time: Optional[datetime]
    author: Optional[User]
    discord_message_id: Optional[str]
    updated_at: Optional[datetime]
    title: Optional[str]
    telegram_message_id: Optional[str]
    importance: Optional[ImportanceType]
    images: Optional[list[File]]
    is_published: Optional[bool]
    content: Optional[str]
    created_at: datetime

class NewsSchemaResponse(AwesomeBaseModel):
    """response schema for News model"""

    type: NewsType
    is_pinned: Optional[bool]
    tags: list[str]
    is_archived: Optional[bool]
    id: Optional[int]
    summary: Optional[str]
    author_id: int
    event_time: Optional[datetime]
    discord_message_id: Optional[str]
    updated_at: Optional[datetime]
    title: str
    telegram_message_id: Optional[str]
    importance: ImportanceType
    is_published: Optional[bool]
    content: str
    created_at: datetime

class NewsSchemaUpdate(AwesomeBaseModel):
    """update schema for News model"""

    type: Optional[NewsType]
    is_pinned: Optional[bool]
    tags: Optional[list[str]]
    is_archived: Optional[bool]
    summary: Optional[str]
    author_id: Optional[int]
    event_time: Optional[datetime]
    discord_message_id: Optional[str]
    title: Optional[str]
    telegram_message_id: Optional[str]
    importance: Optional[ImportanceType]
    is_published: Optional[bool]
    content: Optional[str]

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
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    author_id: Optional[int] = None
    min_author_id: Optional[int] = None
    max_author_id: Optional[int] = None
    discord_message_id: Optional[str] = None
    telegram_message_id: Optional[str] = None
    event_time: Optional[datetime] = None
    min_event_time: Optional[datetime] = None
    max_event_time: Optional[datetime] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    type: Optional[NewsType] = None
    importance: Optional[ImportanceType] = None
    images_id: Optional[int] = None

class NewsSort(StrEnum):
    """Enum for sorting the News model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
