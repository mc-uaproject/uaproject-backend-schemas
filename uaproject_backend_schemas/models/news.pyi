# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
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
    author: Optional[User]
    images: Optional[List[NewsImage]]
    schemas: NewsSchemas
    scopes: NewsScopes
    filters: NewsFilters
    sorts: NewsSorts
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

class NewsScopes:
    """Scopes for the News model."""

class NewsFilters:
    """Declarative filters for the News model."""

class NewsFilter(BaseModel):
    """Pydantic-class for filtering the News model."""

class NewsSorts:
    """Declarative sorts for the News model."""

class NewsSort(StrEnum):
    """Enum for sorting the News model."""
