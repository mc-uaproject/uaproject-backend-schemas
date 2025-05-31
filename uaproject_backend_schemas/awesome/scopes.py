from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from .schemas import AwesomeSchemas, FieldsDefinitionBase

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


class AwesomeScopes(AwesomeSchemas):
    """Model Scope manager. Provides methods for getting field configurations."""

    def __init__(
        self,
        model_cls: Type["AwesomeModel"],
        definition: Type[FieldsDefinitionBase] = ScopeDefinition,
        home: str = "Scopes",
    ):
        super().__init__(model_cls, definition, home)

    def __repr__(self):
        cls_name = self.__class__.__name__
        model_name = getattr(self.model_cls, "__name__", str(self.model_cls))
        scopes = self.list()
        return f"<{cls_name} for {model_name}, scopes={scopes}>"
