import inspect
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from .schemas import FieldsDefinitionBase
from .utils import camel_to_snake

if TYPE_CHECKING:
    from .model import AwesomeModel

TModel = TypeVar("TModel", bound="AwesomeModel")


class ScopeDefinition(FieldsDefinitionBase):
    """Base class for Scope definition - a set of fields and access rights for model representation."""

    relationships: Optional[Dict[str, str]] = None
    schema: Optional[str] = None

    def __init__(
        self,
        fields: Optional[List[str]] = None,
        fields_exclude: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        relationships: Optional[Dict[str, str]] = None,
        schema: Optional[str] = None,
    ):
        super().__init__(fields=fields, fields_exclude=fields_exclude, permissions=permissions)
        if relationships is not None:
            self.relationships = relationships
        if schema is not None:
            self.schema = schema

    @classmethod
    def format_permissions(
        cls, permissions: Optional[List[str]], model_cls: Any
    ) -> Optional[List[str]]:
        """Format permissions strings with model class attributes."""
        if not permissions:
            return permissions
        return [p.format(model_cls=model_cls) for p in permissions]


class AwesomeScopes:
    """Model Scope manager. Provides methods for getting field configurations."""

    def __init__(self, model_cls: Type[TModel]):
        self.model_cls = model_cls

        if not hasattr(self.model_cls.Scopes, "Full"):

            class Full(ScopeDefinition):
                permissions = ["{model_cls.__scope_prefix__}.read"]

            setattr(self.model_cls.Scopes, "Full", Full)

    def __list__(self) -> List[str]:
        return self.model_cls.scopes.list()

    @classmethod
    def get(cls, name: str) -> Type[ScopeDefinition]:
        """Get Scope definition by name (snake_case, e.g., 'minecraft_nickname' -> MinecraftNickname class)."""
        attr_name = camel_to_snake(name)
        for attr, value in cls.__dict__.items():
            if (
                camel_to_snake(attr) == attr_name
                and inspect.isclass(value)
                and issubclass(value, ScopeDefinition)
            ):
                return value
        raise AttributeError(f"Scope '{name}' not found in {cls.__name__}")

    @classmethod
    def _get_all_fields(cls, model_cls: Type[TModel]) -> List[str]:
        """Get all model fields including computed fields."""
        fields = []

        if hasattr(model_cls, "model_fields"):
            fields.extend(model_cls.model_fields.keys())
        else:
            fields.extend(model_cls.__annotations__.keys())

        for name, value in inspect.getmembers(model_cls):
            if isinstance(value, property) and getattr(value, "__computed_field__", False):
                fields.append(name)

        return fields

    @classmethod
    def resolve_fields(cls, model_cls: Type[TModel], scope_name: str) -> List[str]:
        """Determine the final list of fields for a given scope, taking into account include/exclude and relationships."""
        scope_def_cls = cls.get(scope_name)
        all_fields = cls._get_all_fields(model_cls)

        if scope_def_cls.schema:
            fields = model_cls.schemas._get_schema_fields(model_cls, scope_def_cls.schema)
        elif scope_def_cls.fields is not None:
            fields = list(scope_def_cls.fields)
        elif scope_def_cls.fields_exclude is not None:
            fields = [f for f in all_fields if f not in scope_def_cls.fields_exclude]
        else:
            fields = all_fields.copy()

        if (
            "id" in all_fields
            and (scope_def_cls.fields_exclude is None or "id" not in scope_def_cls.fields_exclude)
            and "id" not in fields
        ):
            fields.insert(0, "id")

        if hasattr(scope_def_cls, "permissions") and scope_def_cls.permissions:
            scope_def_cls.permissions = ScopeDefinition.format_permissions(
                scope_def_cls.permissions, model_cls
            )

        rels = getattr(model_cls, "__relationships__", [])
        return [f for f in fields if f not in rels]

    @classmethod
    def list(cls) -> List[str]:
        """Get a list of all declared scopes (in snake_case)."""
        scopes: List[str] = []
        for attr_name, attr_value in cls.__dict__.items():
            if attr_name.startswith("_"):
                continue
            if inspect.isclass(attr_value) and issubclass(attr_value, ScopeDefinition):
                if attr_value is ScopeDefinition:
                    continue
                scopes.append(camel_to_snake(attr_name))
        return scopes
