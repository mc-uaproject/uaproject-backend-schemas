import inspect
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel, create_model

from .base_model import AwesomeBaseModel
from .fields import AwesomeFieldInfo
from .utils import camel_to_snake

if TYPE_CHECKING:
    from .model import AwesomeModel

TModel = TypeVar("TModel", bound="AwesomeModel")


class FieldsDefinitionBase:
    fields: Optional[List[str]] = None
    fields_exclude: Optional[List[str]] = None
    permissions: Optional[List[str]] = None

    def __init__(self, fields=None, fields_exclude=None, permissions=None, **kwargs):
        if fields is not None:
            self.fields = fields
        if fields_exclude is not None:
            self.fields_exclude = fields_exclude
        if permissions is not None:
            self.permissions = permissions

    @classmethod
    def format_permissions(cls, permissions, model_cls):
        if not permissions:
            return permissions
        return [p.format(model_cls=model_cls) for p in permissions]


class SchemaDefinition(FieldsDefinitionBase):
    optional: Optional[bool | List[str]] = None

    def __init__(self, fields=None, fields_exclude=None, optional=None, permissions=None):
        super().__init__(fields=fields, fields_exclude=fields_exclude, permissions=permissions)
        if optional is not None:
            self.optional = optional


class AwesomeSchemas:
    """Schema/Pydantic model manager for a specific model class.
    When accessing an attribute, creates (or returns cached) a Pydantic model."""

    def __init__(self, model_cls: Type["AwesomeModel"]):
        self.model_cls = model_cls
        self._cache: Dict[str, Type[BaseModel]] = {}
        self._names: Dict[str, str] = {}

        if not hasattr(self.model_cls.Schemas, "Create"):

            class Create(SchemaDefinition):
                fields_exclude = ["id"]
                optional = True
                permissions = ["{model_cls.__scope_prefix__}.write"]

            setattr(self.model_cls.Schemas, "Create", Create)

        if not hasattr(self.model_cls.Schemas, "Update"):

            class Update(SchemaDefinition):
                fields_exclude = ["id"]
                optional = True
                permissions = ["{model_cls.__scope_prefix__}.write"]

            setattr(self.model_cls.Schemas, "Update", Update)

        if not hasattr(self.model_cls.Schemas, "Response"):

            class Response(SchemaDefinition):
                permissions = ["{model_cls.__scope_prefix__}.read"]

            setattr(self.model_cls.Schemas, "Response", Response)

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
    def _get_schema_fields(cls, model_cls: Type[TModel], schema_name: str) -> List[str]:
        """Get fields from schema."""
        schema_cls = None
        if hasattr(model_cls, "Schemas"):
            for attr in dir(model_cls.Schemas):
                if camel_to_snake(attr) == camel_to_snake(schema_name):
                    schema_cls = getattr(model_cls.Schemas, attr)
                    break
        if schema_cls is None:
            raise AttributeError(f"Schema '{schema_name}' not found")

        all_fields = cls._get_all_fields(model_cls)
        if inspect.isclass(schema_cls) and issubclass(schema_cls, BaseModel):
            return (
                list(schema_cls.model_fields.keys())
                if hasattr(schema_cls, "model_fields")
                else list(schema_cls.__annotations__.keys())
            )
        elif inspect.isclass(schema_cls) and issubclass(schema_cls, SchemaDefinition):
            if schema_cls.fields is not None:
                fields = list(schema_cls.fields)
            elif schema_cls.fields_exclude is not None:
                fields = [f for f in all_fields if f not in schema_cls.fields_exclude]
            else:
                fields = all_fields.copy()
            if (
                "id" in all_fields
                and (schema_cls.fields_exclude is None or "id" not in schema_cls.fields_exclude)
                and "id" not in fields
            ):
                fields.insert(0, "id")
            return fields
        return all_fields.copy()

    def _get_schema_definition(self, name_lower: str) -> Optional[Type[BaseModel]]:
        """Get schema definition."""
        if not hasattr(self.model_cls, "Schemas"):
            return None
        for attr in dir(self.model_cls.Schemas):
            if camel_to_snake(attr) == name_lower:
                schema_attr = getattr(self.model_cls.Schemas, attr)
                if inspect.isclass(schema_attr) and issubclass(schema_attr, BaseModel):
                    return schema_attr
        return None

    def _should_include_field(self, field: Any, permissions: Optional[List[str]] = None) -> bool:
        """Check if field should be included based on permissions."""
        if not hasattr(field, "exclude_permissions") and not hasattr(field, "include_permissions"):
            return True

        if permissions:
            if (
                hasattr(field, "exclude_permissions")
                and field.exclude_permissions
                and any(p in permissions for p in field.exclude_permissions)
            ):
                return False
            if (
                hasattr(field, "include_permissions")
                and field.include_permissions
                and all(p not in permissions for p in field.include_permissions)
            ):
                return False
        return True

    def _get_field_type(
        self, field_name: str, field_type: Any, relationships: Dict[str, str]
    ) -> Any:
        """Get field type considering relationships."""
        if field_name in relationships:
            related_schema_name = relationships[field_name]
            related_schema_class = globals().get(related_schema_name)
            return related_schema_class if related_schema_class is not None else Any
        return field_type

    def _format_permissions(self, permissions: List[str]) -> List[str]:
        """Format permissions strings with model class attributes."""
        if not permissions:
            return permissions
        return [p.format(model_cls=self.model_cls) for p in permissions]

    def _create_schema_model(
        self,
        fields: List[str],
        relationships: Dict[str, str],
        name: str,
        permissions: List[str] = None,
    ) -> Type[AwesomeBaseModel]:
        """Create Pydantic model with permission-based field visibility."""
        formatted_permissions = self._format_permissions(permissions)
        field_definitions = self._get_field_definitions(
            fields, relationships, formatted_permissions
        )
        filtered_fields = self._filter_fields_by_permissions(
            field_definitions, formatted_permissions
        )

        schema_class_name = f"{self.model_cls.__name__}{name.capitalize()}Schema"
        if permissions:
            schema_class_name += "WithPermissions"

        base_model = create_model(
            schema_class_name,
            __base__=AwesomeBaseModel,
            **filtered_fields,
        )

        self._setup_schema_model(base_model, fields, relationships, name, formatted_permissions)
        return base_model

    def _get_field_definitions(
        self, fields: List[str], relationships: Dict[str, str], permissions: List[str] = None
    ) -> Dict[str, Any]:
        field_definitions = {}
        model_field_info = (
            {fname: finfo.annotation for fname, finfo in self.model_cls.model_fields.items()}
            if hasattr(self.model_cls, "model_fields")
            else dict(self.model_cls.__annotations__.items())
        )

        for f in fields:
            if hasattr(self.model_cls, f):
                field = getattr(self.model_cls, f)
                if isinstance(field, property) and getattr(field, "__computed_field__", False):
                    field_type = field.fget.__annotations__.get("return", Any)
                    field_definitions[f] = (field_type, None)
                    continue

            if f not in model_field_info:
                continue

            field = getattr(self.model_cls, f)
            if not self._should_include_field(field, permissions):
                continue

            field_type = self._get_field_type(f, model_field_info[f], relationships)
            field_definitions[f] = (field_type, None)
        return field_definitions

    def _filter_fields_by_permissions(
        self, field_definitions: Dict[str, Any], permissions: List[str] = None
    ) -> Dict[str, Any]:
        filtered_fields = {}
        for f, (t, _) in field_definitions.items():
            if hasattr(self.model_cls, f):
                field = getattr(self.model_cls, f)
                if isinstance(field, property) and getattr(field, "__computed_field__", False):
                    filtered_fields[f] = (t, None)
                    continue

            if f not in self.model_cls.model_fields:
                filtered_fields[f] = (
                    t,
                    AwesomeFieldInfo(annotation=t, required=False, default=None),
                )
                continue

            field_info = self.model_cls.model_fields[f]
            if not isinstance(field_info, AwesomeFieldInfo):
                filtered_fields[f] = (
                    t,
                    AwesomeFieldInfo(annotation=t, required=False, default=None),
                )
                continue

            if permissions:
                if field_info.exclude_permissions and any(
                    p in permissions for p in field_info.exclude_permissions
                ):
                    continue
                if field_info.include_permissions and all(
                    p not in permissions for p in field_info.include_permissions
                ):
                    continue

            new_field_info = AwesomeFieldInfo(
                annotation=t,
                default=field_info.default,
                exclude_permissions=field_info.exclude_permissions,
                include_permissions=field_info.include_permissions,
                **{
                    k: v
                    for k, v in field_info.__dict__.items()
                    if k
                    not in ["annotation", "default", "exclude_permissions", "include_permissions"]
                },
            )
            filtered_fields[f] = (t, new_field_info)
        return filtered_fields

    def _setup_schema_model(
        self,
        base_model: Type[AwesomeBaseModel],
        fields: List[str],
        relationships: Dict[str, str],
        name: str,
        permissions: List[str] = None,
    ):
        base_model._model_father = self.model_cls
        base_model._fields = fields
        base_model._relationships = relationships
        base_model._name = name
        base_model._permissions = permissions

        def with_permissions(cls, permissions: List[str]) -> Type[AwesomeBaseModel]:
            return self._create_schema_model(
                cls._fields, cls._relationships, cls._name, permissions
            )

        base_model.with_permissions = classmethod(with_permissions)

    def __getattr__(self, name: str) -> type[AwesomeBaseModel]:
        """Dynamically create a Pydantic model for the specified representation."""
        if name.startswith("__"):
            raise AttributeError(f"Attribute '{name}' not found")

        name_lower = camel_to_snake(name)
        if name_lower in self._cache:
            return self._cache[name_lower]

        schema_model = self._get_schema_definition(name_lower)
        if schema_model is not None:
            self._cache[name_lower] = schema_model
            self._names[name_lower] = schema_model.__name__
            return schema_model

        schema_cls = None
        for attr in dir(self.model_cls.Schemas):
            if camel_to_snake(attr) == name_lower:
                schema_cls = getattr(self.model_cls.Schemas, attr)
                break
        if schema_cls is None:
            raise AttributeError(
                f"Schema or scope '{name}' not defined in model {self.model_cls.__name__}"
            )

        if hasattr(schema_cls, "permissions") and schema_cls.permissions:
            schema_cls.permissions = SchemaDefinition.format_permissions(
                schema_cls.permissions, self.model_cls
            )

        fields = self._get_schema_fields(self.model_cls, name)
        relationships = getattr(schema_cls, "relationships", {})

        schema_model = self._create_schema_model(fields, relationships, name)
        self._cache[name_lower] = schema_model
        self._names[name_lower] = schema_model.__name__
        return schema_model

    def with_permissions(self, permissions: List[str]) -> Type[BaseModel]:
        """Create a schema with specific permissions."""
        if not hasattr(self, "_current_schema"):
            raise AttributeError("No schema selected")

        name = self._current_schema
        fields = self._get_schema_fields(self.model_cls, name)
        relationships = getattr(
            getattr(self.model_cls.Schemas, name.capitalize()), "relationships", {}
        )

        formatted_permissions = SchemaDefinition.format_permissions(permissions, self.model_cls)
        return self._create_schema_model(fields, relationships, name, formatted_permissions)

    def get(self, name: str) -> Type[BaseModel]:
        """Get Pydantic model by name (alias for attribute access)."""
        return getattr(self, name)

    def list(self) -> list[str]:
        """Get a list of all available schemas (in snake_case)."""
        names = []
        if hasattr(self.model_cls, "Schemas"):
            for attr_name, attr_value in self.model_cls.Schemas.__dict__.items():
                if attr_name.startswith("_"):
                    continue
                if inspect.isclass(attr_value) and (
                    issubclass(attr_value, SchemaDefinition) or issubclass(attr_value, BaseModel)
                ):
                    names.append(camel_to_snake(attr_name))
        return names
