from enum import StrEnum
from typing import TypeVar

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

ModelType = TypeVar("ModelType", bound=AwesomeModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=AwesomeBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=AwesomeBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=AwesomeBaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=AwesomeBaseModel | BaseModel)


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"
