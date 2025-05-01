from enum import Enum
from typing import Optional

from sqlmodel import Field

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import (
    AwesomeField,
    SchemaDefinition,
    ScopeDefinition,
)


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class User(AwesomeModel, table=True):
    """Base user model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = AwesomeField(exclude_permissions=["private"])
    age: int = AwesomeField(include_permissions=["private"])

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id"]

    class Scopes(AwesomeModel.Scopes):
        class Public(ScopeDefinition):
            fields = ["id", "name"]

        class Private(ScopeDefinition):
            fields_exclude = ["age"]

        class Create(ScopeDefinition):
            schema = "create"


if __name__ == "__main__":
    print(User.schemas.create)
    # returned TestModelCreateSchema
    print(User.schemas.create.with_permissions(["private"]))
    # returned TestModelCreateSchemaWithPermissions
