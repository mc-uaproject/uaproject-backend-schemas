from __future__ import annotations

from enum import Enum
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    get_args,
    get_origin,
)

from pydantic import BaseModel
from sqlmodel import SQLModel

from .actions import AwesomeActions
from .events import AwesomeEvents
from .fields import AwesomeFieldInfo
from .filters import AwesomeFilters
from .schemas import AwesomeSchemas
from .sorts import AwesomeSorts

T = TypeVar("T")


def classproperty(fget: Callable[[Type[Any]], T]) -> T:
    class ClassProperty:
        def __init__(self, fget: Callable[[Type[Any]], T]):
            self.fget = fget

        def __get__(self, obj: Any, owner: Type[Any]) -> T:
            return self.fget(owner)

    return ClassProperty(fget)


class AwesomeModel(SQLModel):
    """Base model class extending SQLModel to support Schemas, Actions and Events."""

    class Schemas(AwesomeSchemas):
        """Nested Schemas class - allows defining SchemaDefinition or Pydantic models inside it."""

        pass

    __schemas__: ClassVar[Optional[AwesomeSchemas]] = None
    actions: ClassVar[AwesomeActions]
    events: ClassVar[AwesomeEvents]
    model_fields: ClassVar[dict[str, AwesomeFieldInfo]]
    schemas: ClassVar
    filters: ClassVar
    filter: ClassVar
    sorts: ClassVar
    sort: ClassVar
    model_permissions: ClassVar[set[str]]
    model_schema_permissions: ClassVar[set[str]]
    model_field_permissions: ClassVar[set[str]]

    _property_cache: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def _get_cache_key(cls, property_name: str) -> str:
        """Generate cache key for a property."""
        return f"{cls.__name__}.{property_name}"

    @classmethod
    def _clear_cache(cls, property_name: str = None):
        """Clear cache for specific property or all properties of this class."""
        if property_name:
            key = cls._get_cache_key(property_name)
            cls._property_cache.pop(key, None)
        else:
            prefix = f"{cls.__name__}."
            keys_to_remove = [k for k in cls._property_cache.keys() if k.startswith(prefix)]
            for key in keys_to_remove:
                cls._property_cache.pop(key, None)

    @classmethod
    def _compute_schema_permissions(cls) -> set[str]:
        """Optimized schema permissions computation."""
        permissions = set()
        if not hasattr(cls, "schemas"):
            return permissions

        schema_names = cls.schemas.list()
        for schema_name in schema_names:
            schema_def = cls.schemas._get_schema_definition(schema_name)
            if schema_def and hasattr(schema_def, "permissions") and schema_def.permissions:
                formatted_permissions = schema_def.format_permissions(schema_def.permissions, cls)
                permissions.update(formatted_permissions)
        return permissions

    @classmethod
    def _compute_field_permissions(cls) -> set[str]:
        """Optimized field permissions computation."""
        permissions = set()
        field_permissions_gen = (
            field_info.format_permissions(cls)
            for field_info in cls.model_fields.values()
            if hasattr(field_info, "format_permissions")
        )
        for field_perms in field_permissions_gen:
            permissions.update(field_perms)
        return permissions

    @classmethod
    def _is_json_field(cls, field_name: str) -> bool:
        """Check if field is a JSON field that needs deserialization."""
        if not hasattr(cls, "model_fields") or field_name not in cls.model_fields:
            return False

        field_info = cls.model_fields[field_name]
        if not hasattr(field_info, "sa_column"):
            return False

        sa_column = field_info.sa_column
        if sa_column is None:
            return False

        # Check if it's a JSON column
        return hasattr(sa_column, "type") and "JSON" in str(sa_column.type)

    @classmethod
    def _get_field_type(cls, field_name: str) -> Optional[Type]:
        """Get the expected type for a field from annotations."""
        if not hasattr(cls, "__annotations__"):
            return None

        annotations = cls.__annotations__
        if field_name not in annotations:
            return None

        return annotations[field_name]

    @classmethod
    def _deserialize_list_field(cls, item_type, value):
        if hasattr(item_type, "model_validate") and isinstance(value, list):
            return [
                item_type.model_validate(item) if isinstance(item, dict) else item for item in value
            ]
        return value

    @classmethod
    def _deserialize_optional_field(cls, args, value):
        for arg in args:
            if arg is not type(None) and hasattr(arg, "model_validate"):
                if isinstance(value, dict):
                    return arg.model_validate(value)
        return value

    @classmethod
    def _deserialize_json_field(cls, field_name: str, value: Any) -> Any:
        """Deserialize JSON field value to appropriate Pydantic model."""
        if value is None:
            return value

        field_type = cls._get_field_type(field_name)
        if field_type is None:
            return value

        origin = get_origin(field_type)
        if origin is list or origin is List:
            args = get_args(field_type)
            if not args:
                return value
            item_type = args[0]
            return cls._deserialize_list_field(item_type, value)

        if hasattr(field_type, "model_validate"):
            if isinstance(value, dict):
                return field_type.model_validate(value)
            return value

        if origin is not None and hasattr(origin, "__name__") and origin.__name__ == "Union":
            args = get_args(field_type)
            return cls._deserialize_optional_field(args, value)

        return value

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization hook to deserialize JSON fields."""
        super().model_post_init(__context)

        # Deserialize JSON fields
        for field_name in self.model_fields.keys():
            if self._is_json_field(field_name):
                value = getattr(self, field_name, None)
                if value is not None:
                    deserialized_value = self._deserialize_json_field(field_name, value)
                    setattr(self, field_name, deserialized_value)

    @classproperty
    def schemas(cls) -> AwesomeSchemas | Type[AwesomeSchemas]:
        """Get Schemas instance."""
        cache_key = cls._get_cache_key("schemas")
        if cache_key not in cls._property_cache:
            cls._property_cache[cache_key] = AwesomeSchemas(cls)
        return cls._property_cache[cache_key]

    @classproperty
    def filters(cls) -> None | AwesomeFilters | Type[AwesomeFilters]:
        """Get Filters instance."""
        if not hasattr(cls, "__filters__") or cls.__filters__ is None:
            filters_cls = getattr(cls, "Filters", None)
            if filters_cls:
                cls.__filters__ = filters_cls(cls)
        return getattr(cls, "__filters__", None)

    @classproperty
    def sorts(cls) -> None | AwesomeSorts | Type[AwesomeSorts]:
        """Get Sorts instance."""
        if not hasattr(cls, "__sorts__") or cls.__sorts__ is None:
            sorts_cls = getattr(cls, "Sorts", None)
            if sorts_cls:
                cls.__sorts__ = sorts_cls(cls)
            else:
                from uaproject_backend_schemas.awesome.sorts import AwesomeSorts

                sorts_cls = type(f"{cls.__name__}Sorts", (AwesomeSorts,), {"model_cls": cls})
                setattr(cls, "Sorts", sorts_cls)
                cls.__sorts__ = sorts_cls(cls)
        return getattr(cls, "__sorts__", None)

    @classproperty
    def filter(cls) -> type[BaseModel] | None:
        """Returns a Pydantic-class for filtering this model."""
        filters_cls = getattr(cls, "Filters", None)
        if filters_cls is None:
            from uaproject_backend_schemas.awesome.filters import AwesomeFilters

            filters_cls = type(f"{cls.__name__}Filters", (AwesomeFilters,), {"model_cls": cls})
            setattr(cls, "Filters", filters_cls)
        return filters_cls.get_pydantic_filter_class()

    @classproperty
    def model_permissions(cls) -> set[str]:
        """Get all permissions required by this model (schemas + fields)."""
        cache_key = cls._get_cache_key("model_permissions")
        if cache_key not in cls._property_cache:
            permissions = set()

            schema_permissions = cls._compute_schema_permissions()
            permissions.update(schema_permissions)

            field_permissions = cls._compute_field_permissions()
            permissions.update(field_permissions)

            cls._property_cache[cache_key] = permissions
        return cls._property_cache[cache_key]

    @classproperty
    def model_schema_permissions(cls) -> set[str]:
        """Get permissions required by schemas only (without field permissions)."""
        cache_key = cls._get_cache_key("model_schema_permissions")
        if cache_key not in cls._property_cache:
            cls._property_cache[cache_key] = cls._compute_schema_permissions()
        return cls._property_cache[cache_key]

    @classproperty
    def model_field_permissions(cls) -> set[str]:
        """Get permissions required by fields only (without schema permissions)."""
        cache_key = cls._get_cache_key("model_field_permissions")
        if cache_key not in cls._property_cache:
            cls._property_cache[cache_key] = cls._compute_field_permissions()
        return cls._property_cache[cache_key]

    @classmethod
    def get_all_model_permissions(cls, include_fields: bool = True) -> dict[str, set[str]]:
        """Get permissions for all models."""
        all_permissions = {}

        def get_all_subclasses(cls):
            """Recursively get all subclasses."""
            subclasses = set()
            for subclass in cls.__subclasses__():
                subclasses.add(subclass)
                subclasses.update(get_all_subclasses(subclass))
            return subclasses

        for subclass in get_all_subclasses(cls):
            model_name = subclass.__name__
            if include_fields:
                all_permissions[model_name] = subclass.model_permissions
            else:
                all_permissions[model_name] = subclass.model_schema_permissions

        return all_permissions

    @classproperty
    def sort(cls) -> type[Enum] | None:
        """Returns an Enum-class for sorting this model."""
        sorts_cls = getattr(cls, "Sorts", None)
        if sorts_cls is None:
            from uaproject_backend_schemas.awesome.sorts import AwesomeSorts

            sorts_cls = type(f"{cls.__name__}Sorts", (AwesomeSorts,), {"model_cls": cls})
            setattr(cls, "Sorts", sorts_cls)
        return sorts_cls.get_enum_sort_class()

    def __init_subclass__(cls, **kwargs):
        """Initialize Schemas, Actions, Events subsystems when creating a subclass."""
        super().__init_subclass__(**kwargs)
        cls.actions = AwesomeActions(cls)
        cls.events = AwesomeEvents(cls)
        if not hasattr(cls, "model_fields"):
            cls.model_fields = {}
            for base in cls.__bases__:
                if hasattr(base, "model_fields"):
                    cls.model_fields.update(base.model_fields)

    def __repr__(self):
        cls_name = self.__class__.__name__
        id_val = getattr(self, "id", None)
        field_names = [f for f in getattr(self, "model_fields", {}).keys() if f != "id"]
        field_strs = []
        for name in field_names[:3]:
            val = getattr(self, name, None)
            field_strs.append(f"{name}={val!r}")
        id_part = f" id={id_val}" if id_val is not None else ""
        fields_part = (", " + ", ".join(field_strs)) if field_strs else ""
        return f"<{cls_name}{id_part}{fields_part}>"
