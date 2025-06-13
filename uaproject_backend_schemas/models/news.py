from datetime import datetime
from enum import StrEnum
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
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.models.user import User


class NewsType(StrEnum):
    UPDATE = "update"
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OTHER = "other"
    PERSONAL = "personal"
    CONGRATULATION = "congratulation"
    TECHNICAL = "technical"
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    QUEST = "quest"
    RECRUITMENT = "recruitment"
    HOLIDAY = "holiday"


class ImportanceType(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"
    EMERGENCY = "emergency"


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

    # Social media integration
    discord_message_id: Optional[str] = AwesomeField(max_length=255, nullable=True)
    telegram_message_id: Optional[str] = AwesomeField(max_length=255, nullable=True)

    # Content organization
    tags: List[str] = AwesomeField(sa_column=Column(JSON, nullable=False, default=list))

    # Event-specific fields
    event_time: Optional[datetime] = AwesomeField(sa_column=Column(DateTime, nullable=True))

    # Content management
    is_pinned: bool = AwesomeField(default=False, nullable=False)
    is_archived: bool = AwesomeField(default=False, nullable=False)

    # Classification
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

    # Relationships
    author: Optional[User] = Relationship(back_populates="news")
    images: List[NewsImage] = Relationship(back_populates="news")

    class Schemas:
        class Create(SchemaDefinition):
            fields = ["title", "summary", "content", "type", "importance", "tags", "event_time"]
            fields_exclude = [
                "id",
                "author_id",
                "is_published",
                "discord_message_id",
                "telegram_message_id",
                "is_pinned",
                "is_archived",
                "created_at",
                "updated_at",
            ]

        class Update(SchemaDefinition):
            fields = [
                "title",
                "summary",
                "content",
                "type",
                "importance",
                "tags",
                "event_time",
                "is_published",
                "is_pinned",
                "is_archived",
            ]
            optional = True

        class Response(SchemaDefinition):
            relationships = ["author", "images"]

        class Public(SchemaDefinition):
            fields = [
                "id",
                "title",
                "summary",
                "content",
                "type",
                "importance",
                "tags",
                "event_time",
                "created_at",
                "updated_at",
            ]
            relationships = ["author", "images"]
            fields_exclude = [
                "is_published",
                "discord_message_id",
                "telegram_message_id",
                "is_pinned",
                "is_archived",
                "author_id",
            ]

        class List(SchemaDefinition):
            fields = [
                "id",
                "title",
                "summary",
                "type",
                "importance",
                "is_pinned",
                "created_at",
                "updated_at",
            ]
            relationships = ["author"]
            fields_exclude = [
                "content",
                "discord_message_id",
                "telegram_message_id",
                "is_published",
                "is_archived",
                "author_id",
                "tags",
                "event_time",
            ]
