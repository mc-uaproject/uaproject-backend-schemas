from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar

TModel = TypeVar("TModel")


class SortDefinition:
    """
    Base class for declarative description of sorting.
    """

    field: Optional[str] = None
    description: Optional[str] = None
    direction: Optional[str] = "asc"

    def __init__(
        self,
        field: Optional[str] = None,
        description: Optional[str] = None,
        direction: Optional[str] = None,
    ):
        if field is not None:
            self.field = field
        if description is not None:
            self.description = description
        if direction is not None:
            self.direction = direction


class AwesomeSorts:
    """
    Manager of sorts for the model. Allows to get all available sorts.
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
            and issubclass(getattr(cls, name), SortDefinition)
        ]

    @classmethod
    def get(cls, name: str) -> Type[SortDefinition]:
        if hasattr(cls, name):
            return getattr(cls, name)
        raise AttributeError(f"Sort '{name}' not found in {cls.__name__}")

    @classmethod
    def get_enum_sort_class(cls) -> Type[Enum]:
        """
        Generates an Enum-class for sorting based on declarative SortDefinition.
        """
        members: Dict[str, Any] = {}
        for sort_name in cls.list():
            sort_cls: Type[SortDefinition] = getattr(cls, sort_name)
            members[sort_name.upper()] = sort_cls.field
        enum_cls: Type[Enum] = Enum(f"{cls.__name__}AutoSort", members)
        return enum_cls
