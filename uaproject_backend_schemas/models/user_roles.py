from typing import TYPE_CHECKING

from sqlmodel import Column, ForeignKey, Integer, Relationship

from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeField

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.role import Role
    from uaproject_backend_schemas.models.user import User


class UserRoles(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "user_roles"

    user_id: int = AwesomeField(sa_column=Column(Integer, ForeignKey("users.id")))
    role_id: int = AwesomeField(sa_column=Column(Integer, ForeignKey("roles.id")))

    user: "User" = Relationship(
        back_populates="roles", sa_relationship_kwargs={"foreign_keys": "[UserRoles.user_id]"}
    )
    role: "Role" = Relationship(
        back_populates="users", sa_relationship_kwargs={"foreign_keys": "[UserRoles.role_id]"}
    )
