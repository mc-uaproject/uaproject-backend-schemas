from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Relationship,
)

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition
from uaproject_backend_schemas.models.schemas.news import ImportanceType, NewsType
from uaproject_backend_schemas.models.user import User

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.file import File


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
    images: List["File"] = Relationship(back_populates="news")

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "author_id", "is_published"]
            optional = True
            permissions = [".write"]

        class Publish(SchemaDefinition):
            fields = ["is_published"]
            permissions = [".admin"]

        class UpdateMeta(SchemaDefinition):
            fields = ["is_pinned", "is_archived", "type", "importance"]
            permissions = [".admin"]

        class Response(SchemaDefinition):
            permissions = [".read"]
