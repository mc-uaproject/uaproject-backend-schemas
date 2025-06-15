# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.news import News

class NewsImage(AwesomeModel):
    """Base newsimage model."""

    id: int
    news_id: int
    image_data: Optional[bytes]
    image_path: Optional[str]
    image_url: Optional[str]
    order: int
    news: Optional[News]
    schemas: NewsImageSchemas
    scopes: NewsImageScopes
    filters: NewsImageFilters
    sorts: NewsImageSorts
    filter: type[NewsImageFilter]
    sort: type[NewsImageSort]

class NewsImageSchemas:
    """Schemas for the NewsImage model."""

    create: NewsImageSchemaCreate
    update: NewsImageSchemaUpdate
    response: NewsImageSchemaResponse

class NewsImageSchemaCreate(AwesomeBaseModel):
    """create schema for NewsImage model"""

    news_id: int
    image_data: Optional[bytes]
    image_path: Optional[str]
    image_url: Optional[str]
    order: int
    news: Optional[News]

class NewsImageSchemaUpdate(AwesomeBaseModel):
    """update schema for NewsImage model"""

    news_id: int
    image_data: Optional[bytes]
    image_path: Optional[str]
    image_url: Optional[str]
    order: int
    news: Optional[News]

class NewsImageSchemaResponse(AwesomeBaseModel):
    """response schema for NewsImage model"""

    id: int
    news_id: int
    image_data: Optional[bytes]
    image_path: Optional[str]
    image_url: Optional[str]
    order: int
    news: Optional[News]

class NewsImageScopes:
    """Scopes for the NewsImage model."""

class NewsImageFilters:
    """Declarative filters for the NewsImage model."""

class NewsImageFilter(BaseModel):
    """Pydantic-class for filtering the NewsImage model."""

class NewsImageSorts:
    """Declarative sorts for the NewsImage model."""

class NewsImageSort(StrEnum):
    """Enum for sorting the NewsImage model."""
