from __future__ import annotations

from typing import Any, Callable, ClassVar, Optional, Type, TypeVar

from sqlmodel import SQLModel

from uaproject_backend_schemas.awesome.actions import AwesomeActions
from uaproject_backend_schemas.awesome.events import AwesomeEvents
from uaproject_backend_schemas.awesome.utils import AwesomeFieldInfo, AwesomeSchemas, AwesomeScopes

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

    @classproperty
    def scopes(cls) -> None | AwesomeScopes | Type[AwesomeScopes]:
        """Get Scopes instance."""
        if cls.__scopes__ is None:
            cls.__scopes__ = getattr(cls, "Scopes", None)
        return cls.__scopes__

    @classproperty
    def schemas(cls) -> AwesomeSchemas | Type[AwesomeSchemas]:
        """Get Schemas instance."""
        if cls.__schemas__ is None:
            cls.__schemas__ = AwesomeSchemas(cls)
        return cls.__schemas__

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
