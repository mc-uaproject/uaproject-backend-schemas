from typing import TYPE_CHECKING

from sqlmodel import Column, ForeignKey, Integer, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.role import Role
    from uaproject_backend_schemas.models.user import User


class UserRoles(AwesomeModel, TimestampsMixin, table=True):
    __tablename__ = "user_roles"

    user_id: int = AwesomeField(sa_column=Column(Integer, ForeignKey("users.id"), primary_key=True))
    role_id: int = AwesomeField(sa_column=Column(Integer, ForeignKey("roles.id"), primary_key=True))

