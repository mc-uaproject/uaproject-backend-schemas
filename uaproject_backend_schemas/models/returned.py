from typing import Optional

from sqlmodel import Field

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel, AwesomeField


class User(AwesomeModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = AwesomeField(exclude_permissions=["private"])
    age: int = AwesomeField(include_permissions=["private"])


class UserModelCreateSchema(AwesomeBaseModel):
    name: str = AwesomeField(exclude_permissions=["private"])
    age: int = AwesomeField(include_permissions=["private"])


class UserModelCreateSchemaWithPermissions(AwesomeBaseModel):
    age: int = AwesomeField(include_permissions=["private"])
