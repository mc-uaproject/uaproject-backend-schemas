from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Column, ForeignKey, Integer, Relationship

from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeField, ScopeDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User


class Token(AwesomeModel, TimestampsMixin, IDMixin, table=True):
    __tablename__ = "user_tokens"
    __scope_prefix__ = "token"
    model_config = {"arbitrary_types_allowed": True}

    token: UUID = AwesomeField(include_permissions=["token.read", "token.write"], default_factory=uuid4, nullable=False, unique=True)

    user_id: int = AwesomeField(sa_column=Column(Integer, ForeignKey("users.id")))
    user: "User" = Relationship(back_populates="token")

    class Scopes(AwesomeModel.Scopes):
        class Full(ScopeDefinition):
            permissions = ["token.read"]
