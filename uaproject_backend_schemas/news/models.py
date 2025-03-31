import logging
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlmodel import Field, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin
from uaproject_backend_schemas.news.schemas import ImportanceType, NewsType
from uaproject_backend_schemas.webhooks.mixins import WebhookPayloadMixin

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User

__all__ = ["News"]
logger = logging.getLogger(__name__)


class News(Base, IDMixin, TimestampsMixin, WebhookPayloadMixin, table=True):
    __tablename__ = "news"
    __scope_prefix__ = "news"

    user_id: int = Field(foreign_key="users.id", nullable=True)

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
