from typing import TYPE_CHECKING, ClassVar, Dict, List, Optional, Type

from pydantic import BaseModel

if TYPE_CHECKING:
    from .fields import AwesomeFieldInfo
    from .model import AwesomeModel


class AwesomeBaseModel(BaseModel):
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
