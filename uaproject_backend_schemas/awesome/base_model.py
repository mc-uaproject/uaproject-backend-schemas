import datetime
import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, Dict, List, Optional, Type

from pydantic import BaseModel

if TYPE_CHECKING:
    from .fields import AwesomeFieldInfo
    from .model import AwesomeModel


class AwesomeBaseModel(BaseModel):
    model_config = {
        "ser_json_encoders": {
            Decimal: str,
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat(),
            datetime.time: lambda v: v.isoformat(),
            uuid.UUID: str,
        }
    }
    _model_father: ClassVar[Type["AwesomeModel"]] = None
    _fields: ClassVar[List[str]] = []
    _relationships: ClassVar[Dict[str, str]] = {}
    _name: ClassVar[str] = ""
    _permissions: ClassVar[Optional[List[str]]] = None
    model_fields: ClassVar[dict[str, "AwesomeFieldInfo"]]

    @classmethod
    def _create_model(
        cls, target_model: Type["AwesomeBaseModel"], permissions: Optional[List[str]] = None, **data
    ) -> Type["AwesomeBaseModel"]:
        """Create a new model instance with specific permissions."""
        return cls._model_father.schemas._create_schema_model(
            cls._fields, cls._relationships, cls._name, permissions
        )

    @classmethod
    def with_permissions(
        cls, target_model: Type["AwesomeBaseModel"], permissions: List[str], **data
    ) -> Type["AwesomeBaseModel"]:
        """Create a new model instance with specific permissions."""
        return cls._create_model(target_model, permissions, **data)

    @classmethod
    def __call__(cls, *args, **kwargs) -> Type["AwesomeBaseModel"]:
        """Create a new model instance."""
        return cls._create_model(cls, cls._permissions, **kwargs)

    def to_json(self, **kwargs) -> str:
        """Serialize model to JSON with support for decimal, datetime, uuid, etc."""
        return self.model_dump_json(**kwargs)

    @classmethod
    def from_json(cls, json_str: str, **kwargs) -> "AwesomeBaseModel":
        """Deserialize JSON into AwesomeBaseModel with support for decimal, datetime, uuid, etc."""
        return cls.model_validate_json(json_str, **kwargs)
