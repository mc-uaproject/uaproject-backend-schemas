from datetime import datetime
from typing import List, Optional

from sqlmodel import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    LargeBinary,
    Relationship,
)

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.schemas.news import ImportanceType, NewsType
from uaproject_backend_schemas.models.user import User


class NewsImage(AwesomeModel, IDMixin, table=True):
    __tablename__ = "news_images"
    __scope_prefix__ = "news_image"
    model_config = {"arbitrary_types_allowed": True}

    news_id: int = AwesomeField(sa_column=Column(BigInteger, ForeignKey("news.id"), nullable=False))
    image_data: Optional[bytes] = AwesomeField(sa_column=Column(LargeBinary, nullable=True))
    image_path: Optional[str] = AwesomeField(max_length=512, nullable=True)
    image_url: Optional[str] = AwesomeField(max_length=512, nullable=True)
    order: int = AwesomeField(default=0, nullable=False)

    news: Optional["News"] = Relationship(back_populates="images")


class News(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "news"
    __scope_prefix__ = "news"
    model_config = {"arbitrary_types_allowed": True}

    title: str = AwesomeField(max_length=255, nullable=False)
    summary: Optional[str] = AwesomeField(max_length=500, nullable=True)
    content: str = AwesomeField(nullable=False)
    is_published: bool = AwesomeField(default=False, nullable=False)
    author_id: int = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("users.id"), nullable=False)
    )

    discord_message_id: Optional[str] = AwesomeField(max_length=255, nullable=True)
    telegram_message_id: Optional[str] = AwesomeField(max_length=255, nullable=True)

    tags: List[str] = AwesomeField(sa_column=Column(JSON, nullable=False, default=list))

    event_time: Optional[datetime] = AwesomeField(sa_column=Column(DateTime, nullable=True))

    is_pinned: bool = AwesomeField(default=False, nullable=False)
    is_archived: bool = AwesomeField(default=False, nullable=False)

    type: NewsType = AwesomeField(
        sa_column=Column(
            Enum(NewsType, native_enum=False),
            default=NewsType.INFO,
            server_default=NewsType.INFO,
        )
    )
    importance: ImportanceType = AwesomeField(
        sa_column=Column(
            Enum(ImportanceType, native_enum=False),
            default=ImportanceType.MEDIUM,
            server_default=ImportanceType.MEDIUM,
        )
    )

    author: Optional[User] = Relationship(back_populates="news")
    images: List[NewsImage] = Relationship(back_populates="news")
