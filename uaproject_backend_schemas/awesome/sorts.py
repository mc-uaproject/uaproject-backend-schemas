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
        members = cls._get_custom_sort_members()

        if not members and hasattr(cls, "model_cls"):
            members = cls._get_default_sort_members()

        enum_cls: Type[Enum] = Enum(f"{cls.__name__}AutoSort", members)
        return enum_cls

    @classmethod
    def _get_custom_sort_members(cls) -> Dict[str, Any]:
        """Get sort members from custom sort definitions"""
        members: Dict[str, Any] = {}
        for sort_name in cls.list():
            sort_cls: Type[SortDefinition] = getattr(cls, sort_name)
            members[sort_name.upper()] = sort_cls.field
        return members

    @classmethod
    def _get_default_sort_members(cls) -> Dict[str, Any]:
        """Get default sort members for common fields"""
        all_fields = cls._get_model_fields() + cls._get_computed_fields()
        return cls._create_sort_members_for_fields(all_fields)

    @classmethod
    def _get_model_fields(cls) -> List[str]:
        """Get regular model fields"""
        if hasattr(cls.model_cls, "model_fields"):
            return list(cls.model_cls.model_fields.keys())
        elif hasattr(cls.model_cls, "__annotations__"):
            return list(cls.model_cls.__annotations__.keys())
        return []

    @classmethod
    def _get_computed_fields(cls) -> List[str]:
        """Get computed fields from the model"""
        computed_fields = []

        if hasattr(cls.model_cls, "model_computed_fields"):
            computed_fields = list(cls.model_cls.model_computed_fields.keys())

        computed_fields.extend(cls._find_computed_properties(computed_fields))
        return computed_fields

    @classmethod
    def _find_computed_properties(cls, existing_computed: List[str]) -> List[str]:
        """Find computed properties in the model"""
        computed_fields = []
        for attr_name in dir(cls.model_cls):
            if attr_name.startswith("_") or attr_name in existing_computed:
                continue

            try:
                attr = getattr(cls.model_cls, attr_name)
                if cls._is_computed_property(attr):
                    computed_fields.append(attr_name)
            except (AttributeError, RecursionError, ImportError):
                continue
        return computed_fields

    @classmethod
    def _is_computed_property(cls, attr) -> bool:
        """Check if an attribute is a Pydantic computed property"""
        if not isinstance(attr, property):
            return False

        fget = getattr(attr, "fget", None)
        if not fget or not hasattr(fget, "decorator_info"):
            return False

        try:
            from pydantic.fields import ComputedFieldInfo

            return isinstance(getattr(fget, "decorator_info", None), ComputedFieldInfo)
        except ImportError:
            return False

    @classmethod
    def _create_sort_members_for_fields(cls, all_fields: List[str]) -> Dict[str, Any]:
        """Create sort enum members for common sortable fields"""
        members: Dict[str, Any] = {}
        common_sortable_fields = ["id", "created_at", "updated_at", "name", "title"]

        for field in common_sortable_fields:
            if field in all_fields:
                members[field.upper()] = field
        return members
