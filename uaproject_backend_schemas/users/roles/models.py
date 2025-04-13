from typing import TYPE_CHECKING, List

from sqlmodel import JSON, BigInteger, Column, Field, Relationship

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin

if TYPE_CHECKING:
    from uaproject_backend_schemas.users.models import User

__all__ = ["Role", "UserRoles"]


class UserRoles(Base, table=True):
    __tablename__ = "user_roles"
    user_id: int = Field(foreign_key="users.id", sa_column=Column(BigInteger()), primary_key=True)
    role_id: int = Field(foreign_key="roles.id", sa_column=Column(BigInteger()), primary_key=True)


class Role(Base, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "roles"

    name: str = Field(unique=True, index=True)
    display_name: str | None = Field(default=None, nullable=True)
    permissions: List[str] = Field(sa_column=Column(JSON))
    weight: int = Field(default=0, index=True)

    users: List["User"] = Relationship(
        back_populates="roles", sa_relationship_kwargs={"secondary": UserRoles.__table__}
    )
