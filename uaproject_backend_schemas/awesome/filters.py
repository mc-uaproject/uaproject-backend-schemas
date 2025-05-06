from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel, create_model

TModel = TypeVar("TModel")


class FilterDefinition:
    """
    Base class for declarative description of a filter.
    """

    field: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Any] = None

    def __init__(
        self,
        field: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[Any] = None,
    ):
        if field is not None:
            self.field = field
        if description is not None:
            self.description = description
        if type is not None:
            self.type = type


class AwesomeFilters:
    """
    Manager of filters for the model. Allows to get all available filters.
    """

    def __init__(self, model_cls: Type[TModel]):
        self.model_cls: Type[TModel] = model_cls

    @classmethod
    def list(cls) -> List[str]:
        return [
            name
            for name in dir(cls)
            if not name.startswith("_")
            and isinstance(getattr(cls, name), type)
            and issubclass(getattr(cls, name), FilterDefinition)
        ]

    @classmethod
    def get(cls, name: str) -> Type[FilterDefinition]:
        if hasattr(cls, name):
            return getattr(cls, name)
        raise AttributeError(f"Filter '{name}' not found in {cls.__name__}")

    @classmethod
    def get_pydantic_filter_class(cls) -> Type[BaseModel]:
        """
        Generates a Pydantic-class for filtering based on declarative FilterDefinition.
        """
        fields: Dict[str, Any] = {}
        for filter_name in cls.list():
            filter_cls: Type[FilterDefinition] = getattr(cls, filter_name)
            typ: Any = getattr(filter_cls, "type", None) or Optional[Any]
            fields[filter_cls.field] = (typ, None)
        model: Type[BaseModel] = create_model(f"{cls.__name__}AutoFilter", **fields)
        return model
