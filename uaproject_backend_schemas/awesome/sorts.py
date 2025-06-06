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
        
        # Add custom sort definitions
        for sort_name in cls.list():
            sort_cls: Type[SortDefinition] = getattr(cls, sort_name)
            members[sort_name.upper()] = sort_cls.field
        
        # If no custom sorts defined, add default sorts for common fields
        if not members and hasattr(cls, 'model_cls'):
            model_fields = []
            computed_fields = []
            
            # Get regular model fields
            if hasattr(cls.model_cls, "model_fields"):
                model_fields = list(cls.model_cls.model_fields.keys())
            elif hasattr(cls.model_cls, "__annotations__"):
                model_fields = list(cls.model_cls.__annotations__.keys())
            
            # Get computed fields (like created_at) from Pydantic model_computed_fields
            if hasattr(cls.model_cls, 'model_computed_fields'):
                computed_fields = list(cls.model_cls.model_computed_fields.keys())
            
            # Also check for properties with ComputedFieldInfo (for Pydantic computed fields)
            for attr_name in dir(cls.model_cls):
                if not attr_name.startswith('_') and attr_name not in computed_fields:
                    try:
                        attr = getattr(cls.model_cls, attr_name)
                        if isinstance(attr, property):
                            # Check if it's a Pydantic computed field
                            fget = getattr(attr, 'fget', None)
                            if fget and hasattr(fget, 'decorator_info'):
                                from pydantic.fields import ComputedFieldInfo
                                if isinstance(getattr(fget, 'decorator_info', None), ComputedFieldInfo):
                                    computed_fields.append(attr_name)
                    except (AttributeError, RecursionError, ImportError):
                        # Skip attributes that cause issues
                        continue
            
            # Combine all available fields
            all_fields = model_fields + computed_fields
            
            # Add common sortable fields with separate ASC/DESC options
            common_sortable_fields = ['id', 'created_at', 'updated_at', 'name', 'title']
            for field in common_sortable_fields:
                if field in all_fields:
                    members[f"{field.upper()}_ASC"] = field
                    members[f"{field.upper()}_DESC"] = f"-{field}"
        
        enum_cls: Type[Enum] = Enum(f"{cls.__name__}AutoSort", members)
        return enum_cls
