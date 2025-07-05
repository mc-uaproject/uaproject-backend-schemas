from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import BigInteger
from sqlmodel import Column, ForeignKey, Index, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User


class UserToken(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "user_tokens"
    __scope_prefix__ = "token"
    __table_args__ = (
        Index("ix_user_tokens_user_id", "user_id"),
        Index("ix_user_tokens_token", "token"),
    )

    token: UUID = AwesomeField(
        read_permissions=["token.read"],
        write_permissions=["token.write"],
        default_factory=uuid4,
        nullable=False,
        unique=True,
    )

    user_id: int = AwesomeField(sa_column=Column(BigInteger, ForeignKey("users.id")))
    user: "User" = Relationship(back_populates="token")
