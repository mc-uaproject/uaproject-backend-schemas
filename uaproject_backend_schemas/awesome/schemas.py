import importlib
import inspect
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, create_model

from .base_model import AwesomeBaseModel
from .fields import AwesomeFieldInfo
from .utils import camel_to_snake, snake_to_camel

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
        formatted = []
        for p in permissions:
            if p.startswith("."):
                prefix = getattr(model_cls, "__scope_prefix__", model_cls.__name__.lower())
                p = f"{prefix}{p}"
            formatted_p = p.format(model_cls=model_cls)
            formatted.append(formatted_p)
        return formatted


class SchemaDefinition(FieldsDefinitionBase):
    optional: Optional[bool | List[str]] = None
    relationships: Optional[bool | Dict[str, str] | List[str] | tuple] = None

    def __init__(
        self, fields=None, fields_exclude=None, optional=None, permissions=None, relationships=None
    ):
        super().__init__(fields=fields, fields_exclude=fields_exclude, permissions=permissions)
        if optional is not None:
            self.optional = optional
        if relationships is not None:
            self.relationships = relationships


class AwesomeSchemas:
    """Schema/Pydantic model manager for a specific model class.
    When accessing an attribute, creates (or returns cached) a Pydantic model."""

    def __init__(
        self,
        model_cls: Type["AwesomeModel"],
        definition: Type[FieldsDefinitionBase] = SchemaDefinition,
        home: str = "Schemas",
    ):
        self.model_cls = model_cls
        self._cache: Dict[str, Type[BaseModel]] = {}
        self._names: Dict[str, str] = {}
        self._definition = definition
        self._dynamic_types: Dict[str, type] = {}

        if hasattr(self.model_cls, home):
            self._home = getattr(self.model_cls, home)
        else:
            raise AttributeError(f"Model {self.model_cls.__name__} has no attribute {home}")

        # Always create default schemas if they don't exist
        # Custom schemas will override these defaults

        if not hasattr(self._home, "Create"):

            class Create(SchemaDefinition):
                fields_exclude = ["id", "created_at", "updated_at"]
                optional = True
                permissions = [".write"]

            setattr(self._home, "Create", Create)

        if not hasattr(self._home, "Update"):

            class Update(SchemaDefinition):
                fields_exclude = ["id", "created_at", "updated_at"]
                optional = True
                permissions = [".write"]

            setattr(self._home, "Update", Update)

        if not hasattr(self._home, "Response"):

            class Response(SchemaDefinition):
                permissions = [".read"]

            setattr(self._home, "Response", Response)

        if not hasattr(self._home, "Redis"):

            class Redis(SchemaDefinition):
                optional = True
                relationships = True

            setattr(self._home, "Redis", Redis)

    def __iter__(self) -> Iterator[str]:
        return iter(self.model_cls.schemas.list())

    @classmethod
    def _get_all_fields(
        cls, model_cls: Type[TModel], include_relationships: bool = False
    ) -> List[str]:
        """Get all model fields including computed fields. If include_relationships=True, also includes relationship fields."""
        fields = set()

        if hasattr(model_cls, "model_fields"):
            fields.update(model_cls.model_fields.keys())
        else:
            fields.update(model_cls.__annotations__.keys())

        if hasattr(model_cls, "model_computed_fields"):
            fields.update(model_cls.model_computed_fields.keys())
        else:
            for name, value in inspect.getmembers(model_cls):
                if isinstance(value, property) and getattr(value, "__computed_field__", False):
                    fields.add(name)

        if include_relationships:
            # Add relationship fields
            for name, value in inspect.getmembers(model_cls):
                if hasattr(value, "__class__") and value.__class__.__name__ in (
                    "RelationshipProperty",
                    "InstrumentedAttribute",
                ):
                    # Additional check to ensure it's a relationship and not a regular column
                    if hasattr(model_cls, "__table__") and hasattr(model_cls.__table__.c, name):
                        continue  # Skip regular columns
                    fields.add(name)

        return list(fields)

    def _get_schema_fields(
        self, model_cls: Type[TModel], schema_name: str, include_relationships: bool = False
    ) -> List[str]:
        """Get fields from schema."""
        schema_cls = None
        for attr in dir(model_cls.Schemas):
            if camel_to_snake(attr) == camel_to_snake(schema_name):
                schema_cls = getattr(model_cls.Schemas, attr)
                break
        if schema_cls is None:
            raise AttributeError(f"Schema '{schema_name}' not found")

        all_fields = self._get_all_fields(model_cls, include_relationships)
        if inspect.isclass(schema_cls) and issubclass(schema_cls, AwesomeBaseModel):
            return (
                list(schema_cls.model_fields.keys())
                if hasattr(schema_cls, "model_fields")
                else list(schema_cls.__annotations__.keys())
            )
        elif inspect.isclass(schema_cls) and issubclass(schema_cls, self._definition):
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

    def _get_schema_definition(self, name_lower: str) -> Optional[Type[AwesomeBaseModel]]:
        """Get schema definition."""
        for attr in dir(self._home):
            if camel_to_snake(attr) == name_lower:
                schema_attr = getattr(self._home, attr)
                if inspect.isclass(schema_attr) and issubclass(schema_attr, AwesomeBaseModel):
                    return schema_attr
        return None

    def _should_include_field(self, field: Any, permissions: Optional[List[str]] = None) -> bool:
        """Check if field should be included based on permissions."""
        # Check for read permissions (or fallback to required_permissions for legacy)
        read_perms = getattr(field, "read_permissions", [])
        if not read_perms:
            # Legacy fallback
            read_perms = getattr(field, "required_permissions", [])

        if not read_perms:
            return True

        if hasattr(field, "format_permissions"):
            required_permissions = field.format_permissions(self.model_cls, "read")
        else:
            required_permissions = read_perms

        if not permissions:
            # For fields with required permissions but user has no permissions,
            # still include the field but it will get default value during filtering
            return False

        return any(p in permissions for p in required_permissions)

    def _get_field_type(
        self, field_name: str, field_type: Any, relationships: Dict[str, str]
    ) -> Any:
        """Get field type considering relationships and dynamically import related models if needed."""
        if field_name in relationships:
            related_schema_name = relationships[field_name]
            related_schema_class = globals().get(related_schema_name)
            return related_schema_class if related_schema_class is not None else Any

        # Handle ForwardRef
        if hasattr(field_type, "__forward_arg__"):
            class_name = field_type.__forward_arg__
            return self._resolve_forward_ref(class_name)

        origin = getattr(field_type, "__origin__", None)
        args = getattr(field_type, "__args__", ())

        # Handle Union (including Optional which is Union[T, None])
        if origin is Union and args:
            # Check if this is Optional[T] (Union[T, None])
            if len(args) == 2 and type(None) in args:
                # This is Optional[T]
                inner_type = args[0] if args[1] is type(None) else args[1]

                # Handle ForwardRef in Optional
                if hasattr(inner_type, "__forward_arg__"):
                    class_name = inner_type.__forward_arg__
                    resolved_class = self._resolve_forward_ref(class_name)
                    return Optional[resolved_class] if resolved_class else Optional[Any]

                # Recursively resolve inner type
                resolved_inner = self._get_field_type(field_name, inner_type, relationships)
                return Optional[resolved_inner]

        if origin in (list, List) and args:
            inner_type = args[0]

            # Handle ForwardRef in List
            if hasattr(inner_type, "__forward_arg__"):
                class_name = inner_type.__forward_arg__
                resolved_class = self._resolve_forward_ref(class_name)
                return List[resolved_class] if resolved_class else List[Any]

            # For regular types (str, int, etc.), use them as-is
            # Only resolve ForwardRef for custom classes that need importing
            if hasattr(inner_type, "__name__") and not isinstance(inner_type, type(None)):
                # Check if this is a built-in type or standard library type
                if inner_type.__module__ in ("builtins", "datetime", "uuid", "decimal"):
                    return List[inner_type]
                else:
                    # This might be a custom class, try to resolve it
                    class_name = inner_type.__name__
                    resolved_class = self._resolve_forward_ref(class_name)
                    return List[resolved_class] if resolved_class != Any else List[inner_type]

        return field_type

    def _resolve_forward_ref(self, class_name: str) -> Any:
        """Resolve a forward reference to an actual class."""
        # First check if it's already in dynamic types cache
        if class_name in self._dynamic_types:
            return self._dynamic_types[class_name]

        # Convert class name to snake_case for module import
        snake_case_name = camel_to_snake(class_name)

        # Try to import from models using snake_case
        module_name = f"uaproject_backend_schemas.models.{snake_case_name}"
        try:
            module = importlib.import_module(module_name)
            imported_class = getattr(module, class_name)
            self._dynamic_types[class_name] = imported_class
            return imported_class
        except (ModuleNotFoundError, AttributeError):
            pass

        # Fallback: try with class name in lowercase
        module_name = f"uaproject_backend_schemas.models.{class_name.lower()}"
        try:
            module = importlib.import_module(module_name)
            imported_class = getattr(module, class_name)
            self._dynamic_types[class_name] = imported_class
            return imported_class
        except (ModuleNotFoundError, AttributeError):
            pass

        # Try to get from globals (might be imported already)
        if class_name in globals():
            self._dynamic_types[class_name] = globals()[class_name]
            return globals()[class_name]

        # Return Any as fallback
        return Any

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
        optional: Optional[bool | List[str]] = None,
    ) -> Type[AwesomeBaseModel]:
        """Create Pydantic model with permission-based field visibility."""
        formatted_permissions = self._format_permissions(permissions)
        field_definitions = self._get_field_definitions(
            fields, relationships, formatted_permissions, optional
        )
        filtered_fields, computed_fields = self._filter_fields_by_permissions(
            field_definitions, optional
        )

        schema_class_name = f"{self.model_cls.__name__}Schema{snake_to_camel(name)}"
        if permissions:
            schema_class_name += "WithPermissions"

        for k, v in self._dynamic_types.items():
            globals()[k] = v

        base_model = create_model(
            schema_class_name,
            __base__=AwesomeBaseModel,
            **filtered_fields,
        )

        # Add computed fields to the new model
        if computed_fields:
            # Initialize model_computed_fields if it doesn't exist
            if not hasattr(base_model, "model_computed_fields"):
                base_model.model_computed_fields = {}

            # Add computed fields to the model_computed_fields dict and as properties
            for field_name, computed_field_info in computed_fields.items():
                base_model.model_computed_fields[field_name] = computed_field_info

                # For properties with computed field decorator, copy the property directly
                if (
                    hasattr(computed_field_info, "wrapped_property")
                    and computed_field_info.wrapped_property
                ):
                    # This is a property decorated with @computed_field
                    setattr(base_model, field_name, computed_field_info.wrapped_property)
                else:
                    # Fallback for other types of computed fields
                    setattr(base_model, field_name, computed_field_info)

        # Copy model-level validators from the source model
        self._copy_model_validators(base_model)

        # Rebuild model to properly register computed fields and validators
        # This is crucial for validators to be properly registered
        base_model.model_rebuild()
        
        # Force recreation of validator schema to include model validators
        # This ensures that copied model validators are properly compiled
        if hasattr(base_model, '__pydantic_core_schema__'):
            delattr(base_model, '__pydantic_core_schema__')
        if hasattr(base_model, '__pydantic_validator__'):
            delattr(base_model, '__pydantic_validator__')
        
        # Force recompilation by rebuilding again after clearing cache
        base_model.model_rebuild(force=True)

        self._setup_schema_model(base_model, fields, relationships, name, formatted_permissions)

        return base_model

    def _get_field_type_from_annotations(self, f: str) -> Any:
        """Get field type from __annotations__ model, considering Mapped and List."""
        if hasattr(self.model_cls, "__annotations__") and f in self.model_cls.__annotations__:
            field_type = self.model_cls.__annotations__[f]
            origin = getattr(field_type, "__origin__", None)
            if origin is not None and origin.__name__ == "Mapped":
                field_type = field_type.__args__[0]
                origin = getattr(field_type, "__origin__", None)

            # Resolve ForwardRef in field_type
            resolved_field_type = self._get_field_type(f, field_type, {})

            if origin in (list, List):
                return (
                    resolved_field_type,
                    AwesomeFieldInfo(
                        annotation=resolved_field_type, required=False, default_factory=list
                    ),
                )
            else:
                return (resolved_field_type, None)
        return None

    def _get_field_definitions(
        self,
        fields: List[str],
        relationships: Dict[str, str],
        permissions: List[str] = None,
        optional: Optional[bool | List[str]] = None,
    ) -> Dict[str, Any]:
        field_definitions = {}
        model_field_info = (
            {fname: finfo.annotation for fname, finfo in self.model_cls.model_fields.items()}
            if hasattr(self.model_cls, "model_fields")
            else dict(self.model_cls.__annotations__.items())
        )

        for f in fields:
            # Check if it's a computed field first (Pydantic v2)
            if (
                hasattr(self.model_cls, "model_computed_fields")
                and f in self.model_cls.model_computed_fields
            ):
                computed_field = self.model_cls.model_computed_fields[f]
                if hasattr(computed_field, "return_type") and computed_field.return_type:
                    field_type = computed_field.return_type
                else:
                    field_type = Any
                field_definitions[f] = (field_type, None)
                continue
            elif hasattr(self.model_cls, f):
                field = getattr(self.model_cls, f)
                if isinstance(field, property) and getattr(field, "__computed_field__", False):
                    field_type = field.fget.__annotations__.get("return", Any)
                    field_definitions[f] = (field_type, None)
                    continue

            if f not in model_field_info:
                result = self._get_field_type_from_annotations(f)
                if result is not None:
                    field_definitions[f] = result
                continue

            field = getattr(self.model_cls, f)
            if not self._should_include_field(field, permissions):
                continue

            # Prefer type annotation over model_field_info to avoid SQLAlchemy column types
            if hasattr(self.model_cls, "__annotations__") and f in self.model_cls.__annotations__:
                field_type = self._get_field_type(
                    f, self.model_cls.__annotations__[f], relationships
                )
            else:
                field_type = self._get_field_type(f, model_field_info[f], relationships)
            
            # Pass the original field info if it exists so metadata can be preserved
            original_field_info = None
            if hasattr(self.model_cls, "model_fields") and f in self.model_cls.model_fields:
                original_field_info = self.model_cls.model_fields[f]
                
                # If field has metadata, create an Annotated type to preserve validators
                if hasattr(original_field_info, 'metadata') and original_field_info.metadata:
                    from typing import Annotated
                    field_type = Annotated[field_type, *original_field_info.metadata]
            
            field_definitions[f] = (field_type, original_field_info)
        return field_definitions

    def _is_computed_field(self, field_name: str) -> bool:
        """Check if a field is a computed field."""
        if (
            hasattr(self.model_cls, "model_computed_fields")
            and field_name in self.model_cls.model_computed_fields
        ):
            return True
        if hasattr(self.model_cls, field_name):
            field = getattr(self.model_cls, field_name)
            if isinstance(field, property) and getattr(field, "__computed_field__", False):
                return True
        return False

    def _get_field_info_params(
        self, f: str, field_info: AwesomeFieldInfo, optional: Optional[bool | List[str]]
    ) -> dict:
        """Get parameters for AwesomeFieldInfo."""
        field_default = field_info.default
        field_default_factory = getattr(field_info, "default_factory", None)
        field_required = getattr(field_info, "is_required", lambda: True)()

        from sqlmodel.main import Undefined

        is_field_optional = optional is True or (isinstance(optional, list) and f in optional)
        if is_field_optional:
            field_required = False
            if (
                field_default is None or field_default is Undefined
            ) and field_default_factory is None:
                field_default = None

        return {
            "required": field_required,
            "default": field_default,
            "default_factory": field_default_factory,
        }

    def _build_new_field_info(
        self, t: Any, field_info: AwesomeFieldInfo, params: dict
    ) -> AwesomeFieldInfo:
        """Build a new AwesomeFieldInfo instance."""
        field_args = {
            "annotation": t,
            "read_permissions": getattr(field_info, "read_permissions", []),
            "write_permissions": getattr(field_info, "write_permissions", []),
            **params,
        }

        # Add other attributes from field_info
        excluded_keys = {
            "annotation",
            "default",
            "default_factory",
            "required",
            "read_permissions",
            "write_permissions",
        }
        field_args.update({k: v for k, v in field_info.__dict__.items() if k not in excluded_keys})
        
        # Copy metadata which contains validators and constraints
        if hasattr(field_info, "metadata"):
            field_args["metadata"] = field_info.metadata
            
        return AwesomeFieldInfo(**field_args)

    def _filter_fields_by_permissions(
        self,
        field_definitions: Dict[str, Any],
        optional: Optional[bool | List[str]] = None,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        filtered_fields = {}
        computed_fields = {}

        for f, (t, _) in field_definitions.items():
            if self._is_computed_field(f):
                # Get the actual computed field from the model class
                if (
                    hasattr(self.model_cls, "model_computed_fields")
                    and f in self.model_cls.model_computed_fields
                ):
                    computed_fields[f] = self.model_cls.model_computed_fields[f]
                elif hasattr(self.model_cls, f):
                    field = getattr(self.model_cls, f)
                    if isinstance(field, property) and hasattr(field, "__computed_field__"):
                        computed_fields[f] = field
                continue

            # Check if we have original field info passed from _get_field_definitions
            if _ is not None and isinstance(_, AwesomeFieldInfo):
                # We have original field info, use it to build new field info with metadata
                params = self._get_field_info_params(f, _, optional)
                new_field_info = self._build_new_field_info(t, _, params)
                filtered_fields[f] = (t, new_field_info)
            elif f not in self.model_cls.model_fields or not isinstance(
                self.model_cls.model_fields[f], AwesomeFieldInfo
            ):
                if _ is not None:
                    filtered_fields[f] = (t, _)
                else:
                    filtered_fields[f] = (
                        t,
                        AwesomeFieldInfo(annotation=t, required=False, default=None),
                    )
                continue
            else:
                field_info = self.model_cls.model_fields[f]

                # Note: We include all fields in schema, but field permission filtering
                # happens at runtime in PermissionChecker.apply_field_permissions_to_data
                params = self._get_field_info_params(f, field_info, optional)
                new_field_info = self._build_new_field_info(t, field_info, params)
                filtered_fields[f] = (t, new_field_info)

        return filtered_fields, computed_fields

    def _copy_model_validators(self, target_model: Type[AwesomeBaseModel]) -> None:
        """Copy model-level validators from source model to target model"""
        
        # Copy the full __pydantic_decorators__ registry
        if hasattr(self.model_cls, '__pydantic_decorators__'):
            source_decorators = self.model_cls.__pydantic_decorators__
            
            # Initialize target decorators if not exists
            if not hasattr(target_model, '__pydantic_decorators__'):
                from pydantic._internal._decorators import DecoratorInfos
                target_model.__pydantic_decorators__ = DecoratorInfos()
            
            target_decorators = target_model.__pydantic_decorators__
            
            # Copy model validators
            if hasattr(source_decorators, 'model_validators') and source_decorators.model_validators:
                target_decorators.model_validators.update(source_decorators.model_validators)
                
                # Also copy the actual validator methods
                for validator_name, decorator_info in source_decorators.model_validators.items():
                    if hasattr(self.model_cls, validator_name):
                        validator_method = getattr(self.model_cls, validator_name)
                        setattr(target_model, validator_name, validator_method)
            
            # Copy field validators
            if hasattr(source_decorators, 'field_validators') and source_decorators.field_validators:
                target_decorators.field_validators.update(source_decorators.field_validators)
                
                # Also copy the actual validator methods
                for field_name, field_validators in source_decorators.field_validators.items():
                    for decorator_info in field_validators:
                        validator_name = decorator_info.cls_var_name
                        if hasattr(self.model_cls, validator_name):
                            validator_method = getattr(self.model_cls, validator_name)
                            setattr(target_model, validator_name, validator_method)
            
            # Copy other decorators like computed fields, serializers, etc.
            if hasattr(source_decorators, 'computed_fields') and source_decorators.computed_fields:
                target_decorators.computed_fields.update(source_decorators.computed_fields)
            
            if hasattr(source_decorators, 'field_serializers') and source_decorators.field_serializers:
                target_decorators.field_serializers.update(source_decorators.field_serializers)
            
            if hasattr(source_decorators, 'model_serializers') and source_decorators.model_serializers:
                target_decorators.model_serializers.update(source_decorators.model_serializers)

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

    def _resolve_schema_fields_and_relationships(self, name: str):
        # Find schema class by name (case-insensitive)
        schema_cls = None
        for attr in dir(self._home):
            if camel_to_snake(attr) == camel_to_snake(name):
                schema_cls = getattr(self._home, attr)
                break
        if schema_cls is None:
            raise AttributeError(f"Schema '{name}' not found")

        relationships = getattr(schema_cls, "relationships", {})
        include_relationship_fields = relationships is True
        fields = self._get_schema_fields(self.model_cls, name, include_relationship_fields)
        if relationships is None:
            relationships = {}
        elif relationships is True:
            relationships = {}
            for name_field, value in inspect.getmembers(self.model_cls):
                if hasattr(value, "__class__") and value.__class__.__name__ in (
                    "RelationshipProperty",
                    "InstrumentedAttribute",
                ):
                    # Additional check to ensure it's a relationship and not a regular column
                    if hasattr(self.model_cls, "__table__") and hasattr(
                        self.model_cls.__table__.c, name_field
                    ):
                        continue  # Skip regular columns
                    relationships[name_field] = name_field
        elif (
            not isinstance(relationships, dict)
            and not isinstance(relationships, list)
            and not isinstance(relationships, tuple)
        ):
            raise ValueError("Relationships must be True, a dictionary, list or tuple")
        return fields, relationships, getattr(schema_cls, "optional", None)

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
        for attr in dir(self._home):
            if camel_to_snake(attr) == name_lower:
                schema_cls = getattr(self._home, attr)
                break
        if schema_cls is None:
            raise AttributeError(f"Schema '{name}' not defined in model {self.model_cls.__name__}")

        if hasattr(schema_cls, "permissions") and schema_cls.permissions:
            schema_cls.permissions = self._definition.format_permissions(
                schema_cls.permissions, self.model_cls
            )

        fields, relationships, optional = self._resolve_schema_fields_and_relationships(name)
        schema_model = self._create_schema_model(fields, relationships, name, optional=optional)
        self._cache[name_lower] = schema_model
        self._names[name_lower] = schema_model.__name__
        return schema_model

    def with_permissions(self, permissions: List[str]) -> Type[BaseModel]:
        """Create a schema with specific permissions."""
        if not hasattr(self, "_current_schema"):
            raise AttributeError("No schema selected")

        name = self._current_schema
        fields, relationships, _ = self._resolve_schema_fields_and_relationships(name)
        formatted_permissions = self._definition.format_permissions(permissions, self.model_cls)
        return self._create_schema_model(fields, relationships, name, formatted_permissions)

    def get(self, name: str) -> Type[FieldsDefinitionBase]:
        """Get Pydantic model by name (alias for attribute access)."""
        return getattr(self, name)

    def list(self) -> list[str]:
        """Get a list of all available schemas (in snake_case)."""
        names = []

        # Use dir() instead of __dict__ to catch all attributes including those set by setattr
        for attr_name in dir(self._home):
            if attr_name.startswith("_"):
                continue

            if not hasattr(self._home, attr_name):
                continue

            attr_value = getattr(self._home, attr_name)

            if inspect.isclass(attr_value) and (
                issubclass(attr_value, self._definition)
                or issubclass(attr_value, SchemaDefinition)
                or issubclass(attr_value, BaseModel)
            ):
                names.append(camel_to_snake(attr_name))
        return names

    def __repr__(self):
        cls_name = self.__class__.__name__
        model_name = getattr(self.model_cls, "__name__", str(self.model_cls))
        schemas = self.list()
        return f"<{cls_name} for {model_name}, schemas={schemas}>"
