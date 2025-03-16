from typing import List

from sqlmodel import JSON, Column, Field

from uaproject_backend_schemas.base import Base, IDMixin, TimestampsMixin

__all__ = ["Role", "UserRoles"]


class Role(Base, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "roles"

    name: str = Field(unique=True, index=True)
    display_name: str | None = Field(default=None, nullable=True)
    permissions: List[str] = Field(sa_column=Column(JSON))
    weight: int = Field(default=0, index=True)


class UserRoles(Base, table=True):
    __tablename__ = "user_roles"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)
