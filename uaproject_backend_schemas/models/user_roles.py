from sqlalchemy import BigInteger
from sqlmodel import Column, ForeignKey, Index

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel


class UserRoles(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "user_roles"
    __scope_prefix__ = "user_roles"
    __table_args__ = (
        Index("ix_user_roles_user_id", "user_id"),
        Index("ix_user_roles_role_id", "role_id"),
    )

    user_id: int = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    )
    role_id: int = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("roles.id"), primary_key=True)
    )
