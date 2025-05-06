from __future__ import annotations

from enum import Enum
from typing import Any, Callable, ClassVar, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

from .actions import AwesomeActions
from .events import AwesomeEvents
from .fields import AwesomeFieldInfo
from .filters import AwesomeFilters
from .schemas import AwesomeSchemas
from .scopes import AwesomeScopes
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
    """Base model class extending SQLModel to support Scopes, Schemas, Actions and Events."""

    class Scopes(AwesomeScopes):
        """Nested Scopes class - defines specific ScopeDefinition inside it."""

        pass

    class Schemas(AwesomeSchemas):
        """Nested Schemas class - allows defining SchemaDefinition or Pydantic models inside it."""

        pass

    __scopes__: ClassVar[Optional[Type[AwesomeScopes]]] = None
    __schemas__: ClassVar[Optional[AwesomeSchemas]] = None
    actions: ClassVar[AwesomeActions]
    events: ClassVar[AwesomeEvents]
    model_fields: ClassVar[dict[str, AwesomeFieldInfo]]
    scopes: ClassVar
    schemas: ClassVar
    filters: ClassVar
    filter: ClassVar
    sorts: ClassVar
    sort: ClassVar

    @classproperty
    def scopes(cls) -> None | AwesomeScopes | Type[AwesomeScopes]:
        """Get Scopes instance."""
        if cls.__scopes__ is None:
            scope_cls = getattr(cls, "Scopes", None)
            if scope_cls:
                cls.__scopes__ = scope_cls(cls)
        return cls.__scopes__

    @classproperty
    def schemas(cls) -> AwesomeSchemas | Type[AwesomeSchemas]:
        """Get Schemas instance."""
        if cls.__schemas__ is None:
            cls.__schemas__ = AwesomeSchemas(cls)
        return cls.__schemas__

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
        return getattr(cls, "__sorts__", None)

    @classproperty
    def filter(cls) -> type[BaseModel] | None:
        """Returns a Pydantic-class for filtering this model."""
        if hasattr(cls, "Filters"):
            return cls.Filters.get_pydantic_filter_class()
        return None

    @classproperty
    def sort(cls) -> type[Enum] | None:
        """Returns an Enum-class for sorting this model."""
        if hasattr(cls, "Sorts"):
            return cls.Sorts.get_enum_sort_class()
        return None

    def __init_subclass__(cls, **kwargs):
        """Initialize Scopes, Schemas, Actions, Events subsystems when creating a subclass."""
        super().__init_subclass__(**kwargs)
        cls.actions = AwesomeActions(cls)
        cls.events = AwesomeEvents(cls)
        if not hasattr(cls, "model_fields"):
            cls.model_fields = {}
            for base in cls.__bases__:
                if hasattr(base, "model_fields"):
                    cls.model_fields.update(base.model_fields)
