from typing import TypeVar

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel

ModelType = TypeVar("ModelType", bound=AwesomeModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=AwesomeBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=AwesomeBaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=AwesomeBaseModel)
