from typing import TYPE_CHECKING, Dict, List, Optional

from sqlmodel import JSON, Column, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User


class Role(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "roles"
    __scope_prefix__ = "role"

    name: str = AwesomeField(max_length=100)
    display_name: Optional[str] = AwesomeField(default=None)
    permissions: List[Dict[str, bool]] = AwesomeField(default=[], sa_column=Column(JSON))
    weight: int = AwesomeField(default=0)

    users: List["User"] = Relationship(
        back_populates="roles",
        sa_relationship_kwargs={
            "secondary": "user_roles",
            "lazy": "select"
        },
    )
