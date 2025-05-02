from __future__ import annotations

import inspect
import re
from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)
from urllib.parse import urlparse

from pydantic import BaseModel, GetCoreSchemaHandler, create_model
from pydantic_core import CoreSchema, core_schema
from sqlmodel.main import Column, OnDeleteType, Undefined, UndefinedType, post_init_field_info
from sqlmodel.main import FieldInfo as SQLModelFieldInfo

if TYPE_CHECKING:
    from uaproject_backend_schemas.awesome.model import AwesomeModel

if TYPE_CHECKING:
    from pydantic._internal._model_construction import ModelMetaclass as ModelMetaclass
    from pydantic._internal._repr import Representation as Representation
    from pydantic_core import PydanticUndefined as Undefined
    from pydantic_core import PydanticUndefinedType as UndefinedType

TModel = TypeVar("TModel", bound="AwesomeModel")
NoArgAnyCallable = Callable[[], Any]


class ScopeDefinition:
    """Base class for Scope definition - a set of fields and access rights for model representation."""

    fields: Optional[List[str]] = None
    fields_exclude: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
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
        if fields is not None:
            self.fields = fields
        if fields_exclude is not None:
            self.fields_exclude = fields_exclude
        if permissions is not None:
            self.permissions = permissions
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


class SchemaDefinition:
    """Base class for Schema definition - a set of fields for model data representation."""

    fields: Optional[List[str]] = None
    fields_exclude: Optional[List[str]] = None
    optional: Optional[bool | List[str]] = None
    permissions: Optional[List[str]] = None

    def __init__(
        self,
        fields: Optional[List[str]] = None,
        fields_exclude: Optional[List[str]] = None,
        optional: Optional[bool | List[str]] = None,
        permissions: Optional[List[str]] = None,
    ) -> None:
        if fields is not None:
            self.fields = fields
        if fields_exclude is not None:
            self.fields_exclude = fields_exclude
        if optional is not None:
            self.optional = optional
        if permissions is not None:
            self.permissions = permissions

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

    class Full(ScopeDefinition):
        permissions = ["{model_cls.__scope_prefix__}.read"]

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


class AwesomeSchemas:
    """Schema/Pydantic model manager for a specific model class.
    When accessing an attribute, creates (or returns cached) a Pydantic model."""

    class Create(SchemaDefinition):
        fields_exclude = ["id"]
        optional = True
        permissions = ["{model_cls.__scope_prefix__}.write"]

    class Update(SchemaDefinition):
        fields_exclude = ["id"]
        optional = True
        permissions = ["{model_cls.__scope_prefix__}.write"]

    class Response(SchemaDefinition):
        permissions = ["{model_cls.__scope_prefix__}.read"]

    def __init__(self, model_cls: Type[AwesomeModel]):
        self.model_cls = model_cls
        self._cache: Dict[str, Type[BaseModel]] = {}
        self._names: Dict[str, str] = {}

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


class AwesomeFieldInfo(SQLModelFieldInfo):
    """Custom field that extends SQLField with permission-based field visibility."""

    def __init__(
        self,
        *args,
        exclude_permissions: List[str] = None,
        include_permissions: List[str] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.exclude_permissions = exclude_permissions or []
        self.include_permissions = include_permissions or []

    def __repr__(self) -> str:
        parent_repr = super().__repr__()
        attrs = []
        if self.exclude_permissions:
            attrs.append(f"exclude_permissions={self.exclude_permissions}")
        if self.include_permissions:
            attrs.append(f"include_permissions={self.include_permissions}")
        return f"{parent_repr[:-1]}, {', '.join(attrs)})" if attrs else parent_repr


def AwesomeField(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any] = None,
    include: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    exclude_permissions: List[str] = None,
    include_permissions: List[str] = None,
    multiple_of: Optional[float] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    primary_key: Union[bool, UndefinedType] = Undefined,
    foreign_key: Any = Undefined,
    ondelete: Union[OnDeleteType, UndefinedType] = Undefined,
    unique: Union[bool, UndefinedType] = Undefined,
    nullable: Union[bool, UndefinedType] = Undefined,
    index: Union[bool, UndefinedType] = Undefined,
    sa_type: Union[Type[Any], UndefinedType] = Undefined,
    sa_column: Union[Column, UndefinedType] = Undefined,
    sa_column_args: Union[Sequence[Any], UndefinedType] = Undefined,
    sa_column_kwargs: Union[Mapping[str, Any], UndefinedType] = Undefined,
    schema_extra: Optional[Dict[str, Any]] = None,
) -> Any:
    current_schema_extra = schema_extra or {}
    field_info = AwesomeFieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        exclude_permissions=exclude_permissions,
        include_permissions=include_permissions,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        primary_key=primary_key,
        foreign_key=foreign_key,
        ondelete=ondelete,
        unique=unique,
        nullable=nullable,
        index=index,
        sa_type=sa_type,
        sa_column=sa_column,
        sa_column_args=sa_column_args,
        sa_column_kwargs=sa_column_kwargs,
        **current_schema_extra,
    )
    post_init_field_info(field_info)
    return field_info


class AwesomeBaseModel(BaseModel):
    _model_father: ClassVar[Type[AwesomeModel]] = None
    _fields: ClassVar[List[str]] = []
    _relationships: ClassVar[Dict[str, str]] = {}
    _name: ClassVar[str] = ""
    _permissions: ClassVar[Optional[List[str]]] = None
    model_fields: ClassVar[dict[str, AwesomeFieldInfo]]

    @classmethod
    def _create_model(
        cls, target_model: Type[AwesomeBaseModel], permissions: Optional[List[str]] = None, **data
    ) -> Type[AwesomeBaseModel]:
        """Create a new model instance with specific permissions."""
        return cls._model_father.schemas._create_schema_model(
            cls._fields, cls._relationships, cls._name, permissions
        )

    @classmethod
    def with_permissions(
        cls, target_model: Type[AwesomeBaseModel], permissions: List[str], **data
    ) -> Type[AwesomeBaseModel]:
        """Create a new model instance with specific permissions."""
        return cls._create_model(target_model, permissions, **data)

    @classmethod
    def __call__(cls, *args, **kwargs) -> Type[AwesomeBaseModel]:
        """Create a new model instance."""
        return cls._create_model(cls, cls._permissions, **kwargs)


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class SerializableHttpUrl(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        def validate(value: Any) -> str:
            if isinstance(value, str):
                try:
                    result = urlparse(value)
                    if all([result.scheme, result.netloc]):
                        return value
                except Exception:
                    raise ValueError("Invalid HTTP URL")
            elif isinstance(value, cls):
                return value
            raise ValueError("Invalid URL type")

        def serialize(value: Any) -> str:
            return str(value)

        schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.str_schema(),
            ]
        )

        return core_schema.no_info_after_validator_function(
            validate,
            schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize, when_used="json"
            ),
        )

    def __str__(self) -> str:
        return super().__str__()
