import logging
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, Boolean, Column, DateTime, LargeBinary, String
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlmodel import BigInteger, Field, ForeignKey, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.news.schemas import ImportanceType, NewsType
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User

__all__ = ["News", "NewsImage"]
logger = logging.getLogger(__name__)


class NewsImage(Base, IDMixin, table=True):
    __tablename__ = "news_images"
    __scope_prefix__ = "news_image"

    news_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("news.id"), nullable=False))
    image_data: bytes = Field(sa_column=Column(LargeBinary, nullable=True))
    image_path: Optional[str] = Field(sa_column=Column(String(512), nullable=True))
    image_url: Optional[str] = Field(sa_column=Column(String(512), nullable=True))
    order: int = Field(sa_column=Column(BigInteger(), nullable=False, default=0))

    news: "News" = Relationship(
        back_populates="images",
        sa_relationship_kwargs={"foreign_keys": "[NewsImage.news_id]"},
    )


class News(Base, IDMixin, TimestampsMixin, WebhookPayloadMixin, table=True):
    __tablename__ = "news"
    __scope_prefix__ = "news"

    user_id: Optional[int] = Field(sa_column=Column(BigInteger(), ForeignKey("users.id"), nullable=True))
    title: str = Field(sa_column=Column(String(255), nullable=False))
    content: str = Field(sa_column=Column(String(4096), nullable=False))
    author: Optional[str] = Field(sa_column=Column(String(255), nullable=True))
    discord_message_id: Optional[str] = Field(sa_column=Column(String(255), nullable=True))
    telegram_message_id: Optional[str] = Field(sa_column=Column(String(255), nullable=True))
    is_weekly_update: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    parent_news_id: Optional[int] = Field(sa_column=Column(BigInteger(), ForeignKey("news.id"), nullable=True))
    tags: List[str] = Field(sa_column=Column(JSON, nullable=False, default=list))
    format_type: str = Field(sa_column=Column(String(20), nullable=False, default="markdown"))
    related_threads: List[str] = Field(sa_column=Column(JSON, nullable=False, default=list))
    event_time: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))
    is_pinned: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    is_archived: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))

    type: NewsType = Field(
        sa_column=Column(
            SQLAlchemyEnum(NewsType, native_enum=False),
            default=NewsType.INFO.value,
            server_default=NewsType.INFO.value,
        )
    )

    importance: ImportanceType = Field(
        sa_column=Column(
            SQLAlchemyEnum(ImportanceType, native_enum=False),
            default=ImportanceType.MEDIUM.value,
            server_default=ImportanceType.MEDIUM.value,
        )
    )

    user: Optional["User"] = Relationship(
        back_populates="news",
        sa_relationship_kwargs={"foreign_keys": "[News.user_id]"},
    )

    parent_news: Optional["News"] = Relationship(
        back_populates="child_news",
        sa_relationship_kwargs={"foreign_keys": "[News.parent_news_id]"},
    )

    child_news: List["News"] = Relationship(
        back_populates="parent_news",
        sa_relationship_kwargs={"foreign_keys": "[News.parent_news_id]"},
    )

    images: List["NewsImage"] = Relationship(
        back_populates="news",
        sa_relationship_kwargs={"foreign_keys": "[NewsImage.news_id]"},
    )
