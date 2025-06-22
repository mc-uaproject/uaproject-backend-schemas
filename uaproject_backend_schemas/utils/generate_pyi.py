import ast
import importlib
import inspect
import os
import re
import subprocess
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, List, Type, Union, get_args, get_origin

from sqlalchemy.orm import Mapped

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import snake_to_camel


def expand_wildcard_modules(module_path: str) -> List[str]:
    """Expand wildcard module paths into a list of actual module paths."""
    if not module_path.endswith(".*"):
        return [module_path]

    base_path = module_path[:-2]
    package_parts = base_path.split(".")
    base_dir = os.path.join(*package_parts)

    workspace_root = Path(__file__).parent.parent.parent
    full_path = workspace_root / base_dir

    if not full_path.is_dir():
        return [module_path]

    modules = []
    for item in full_path.iterdir():
        if item.is_file() and item.name.endswith(".py") and not item.name.startswith("__"):
            module_name = item.stem
            modules.append(f"{base_path}.{module_name}")

    return sorted(modules)


MODEL_MODULES = []
for module in [
    "uaproject_backend_schemas.models.*",
]:
    modules = expand_wildcard_modules(module)
    modules = [m for m in modules if not m.endswith("application_old")]
    MODEL_MODULES.extend(modules)

PYI_HEADER = """# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

"""


def _get_schema_permissions(model_cls: Type[AwesomeModel]) -> set[str]:
    """Get permissions from model schemas."""
    permissions = set()

    if not hasattr(model_cls, "schemas"):
        return permissions

    for schema_name in model_cls.schemas.list():
        schema_def = model_cls.schemas._get_schema_definition(schema_name)
        if hasattr(schema_def, "permissions"):
            for perm in schema_def.permissions:
                formatted_perm = perm.format(model_cls=model_cls)
                permissions.add(formatted_perm)

    return permissions


def get_permissions_from_model(model_cls: Type[AwesomeModel]) -> set[str]:
    """Get all unique permissions from model fields and schemas."""
    permissions = set()

    for field in model_cls.model_fields.values():
        if hasattr(field, "read_permissions"):
            permissions.update(field.read_permissions)
        if hasattr(field, "write_permissions"):
            permissions.update(field.write_permissions)

    permissions.update(_get_schema_permissions(model_cls))

    return permissions


def _check_field_needs(field_info: Any, needs: dict) -> str:
    """Check field needs and update the needs dict."""
    field_type = str(field_info.annotation)
    needs["optional"] |= "Optional" in field_type
    needs["list"] |= "List" in field_type
    needs["dict"] |= "Dict" in field_type
    needs["datetime"] |= "datetime" in field_type
    needs["awesome_field"] |= hasattr(field_info, "read_permissions") or hasattr(
        field_info, "write_permissions"
    )
    return field_type


def _get_enum_name(field_type: Any) -> str | None:
    """Extract enum name from field type if it's an enum."""
    if hasattr(field_type, "__name__"):
        type_name = field_type.__name__
        if any(t in type_name for t in ["Status", "Type"]) and not any(
            t in type_name for t in ["Optional", "List", "Dict"]
        ):
            return type_name
    return None


def _add_imports_from_needs(needs: dict) -> tuple[set[str], set[str]]:
    """Add imports based on needs dictionary."""
    std_lib_imports = set()
    local_imports = set()

    if needs["optional"]:
        std_lib_imports.add("from typing import Optional")
    if needs["list"]:
        std_lib_imports.add("from typing import List")
    if needs["dict"]:
        std_lib_imports.add("from typing import Dict")
    if needs["datetime"]:
        std_lib_imports.add("from datetime import datetime")
    if needs["uuid"]:
        std_lib_imports.add("from uuid import UUID")
    if needs["literal"]:
        std_lib_imports.add("from typing import Literal")
    if needs["awesome_field"]:
        local_imports.add("from uaproject_backend_schemas.awesome.utils import AwesomeField")

    return std_lib_imports, local_imports


def _process_field_imports(
    model_cls: Type[AwesomeModel], fields: list[str]
) -> tuple[set[str], set[str], set[str]]:
    """Process field imports and return sets of imports."""
    model_types = set()
    needs = {
        "optional": False,
        "list": False,
        "dict": False,
        "datetime": False,
        "awesome_field": False,
        "uuid": False,
        "literal": False,
    }

    for field in fields:
        if field not in model_cls.model_fields:
            continue

        field_info = model_cls.model_fields[field]
        field_type = _check_field_needs(field_info, needs)

        if "UUID" in str(field_info.annotation):
            needs["uuid"] = True

        if enum_name := _get_enum_name(field_info.annotation):
            model_types.add(enum_name)

    for name, value in inspect.getmembers(model_cls):
        if isinstance(value, property) and getattr(value, "__computed_field__", False):
            field_type = value.fget.__annotations__.get("return", Any)
            needs["datetime"] |= field_type == datetime
            needs["optional"] |= "Optional" in str(field_type)

    if hasattr(model_cls, "scopes"):
        needs["literal"] = True

    std_lib_imports, local_imports = _add_imports_from_needs(needs)
    return std_lib_imports, local_imports, model_types


def parse_imports_from_py(py_path: str) -> dict[str, str]:
    """Returns a map: name -> full import (string) for all import/from-imports in the file."""
    imports = {}
    with open(py_path, "r") as f:
        tree = ast.parse(f.read(), filename=py_path)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                name = alias.asname or alias.name
                if module:
                    imports[name] = f"from {module} import {alias.name}"
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name
                imports[name] = f"import {alias.name}"
    return imports


def extract_types_recursively(tp, used_types):
    # Handle ForwardRef explicitly
    if hasattr(tp, "__forward_arg__"):
        used_types.add(tp.__forward_arg__)
        return

    if hasattr(tp, "__origin__") and hasattr(tp, "__args__"):
        used_types.add(getattr(tp, "_name", None) or getattr(tp, "__name__", str(tp)))
        for arg in tp.__args__:
            extract_types_recursively(arg, used_types)
    elif hasattr(tp, "__name__"):
        used_types.add(tp.__name__)
    elif isinstance(tp, str):
        used_types.add(tp)


def extract_types_from_fields(model_cls: Type[AwesomeModel], fields: list[str]) -> set:
    used_types = set()
    for field_name in fields:
        ann = _get_field_annotation(model_cls, field_name)
        extract_types_recursively(ann, used_types)
    return used_types


def _find_and_add_imports(types_to_check, std_types, py_imports, imports, already_imported):
    """Finds imports for given types from standard and project sources."""
    for tp in types_to_check:
        if tp in std_types and tp not in already_imported:
            imports.add(std_types[tp])
            already_imported.add(tp)
        elif tp in py_imports and tp not in already_imported:
            imports.add(py_imports[tp])
            already_imported.add(tp)


def _find_enum_imports(name, model_cls, imports, already_imported):
    """Finds special-cased enum imports from schema files."""
    model_name = model_cls.__name__.lower()
    schema_module_path = f"uaproject_backend_schemas.models.schemas.{model_name}"
    try:
        schema_module = importlib.import_module(schema_module_path)
        if hasattr(schema_module, name):
            imports.add(f"from {schema_module_path} import {name}")
            already_imported.add(name)
            return True
    except ImportError:
        pass
    return False


def collect_imports_from_types(used_types, std_types, py_imports, model_cls) -> set:
    imports = set()
    already_imported = set()

    all_types_to_check = set(used_types)
    for tp in used_types:
        matches = re.findall(r'"?([A-Z][a-zA-Z0-9_]*)"?', str(tp))
        for match in matches:
            all_types_to_check.add(match)

    _find_and_add_imports(all_types_to_check, std_types, py_imports, imports, already_imported)

    for name, obj in inspect.getmembers(importlib.import_module(model_cls.__module__)):
        if not (inspect.isclass(obj) and name in used_types and name not in already_imported):
            continue

        if hasattr(obj, "__bases__") and any("Enum" in str(base) for base in obj.__bases__):
            if _find_enum_imports(name, model_cls, imports, already_imported):
                continue

        imports.add(f"from {model_cls.__module__} import {name}")
        already_imported.add(name)
    return imports


def collect_imports_from_generated_content(model_cls, std_types) -> set:
    imports = set()
    all_content = []
    for _type in [("Schema", "schemas"), ("Scope", "scopes")]:
        for schema_key in (
            getattr(model_cls, _type[1], []).list()
            if hasattr(model_cls, _type[1]) and hasattr(getattr(model_cls, _type[1]), "list")
            else []
        ):
            all_content.append(generate_class(model_cls, schema_key, _type=_type[0]))
    content_str = "\n".join(all_content)
    if "AwesomeField(" in content_str:
        imports.add(std_types["AwesomeField"])
    if "Literal[" in content_str:
        imports.add(std_types["Literal"])
    return imports


def get_required_imports(model_cls: Type[AwesomeModel], fields: list[str]) -> set:
    """Automatically gets required imports for .pyi based on types in fields and imports from .py."""
    std_types = {
        "Optional": "from typing import Optional",
        "List": "from typing import List",
        "Dict": "from typing import Dict",
        "Any": "from typing import Any",
        "Literal": "from typing import Literal",
        "UUID": "from uuid import UUID",
        "Decimal": "from decimal import Decimal",
        "datetime": "from datetime import datetime",
        "AwesomeField": "from uaproject_backend_schemas.awesome.fields import AwesomeField",
        "Mapped": "from sqlalchemy.orm import Mapped",
    }
    base_imports = {
        "from uaproject_backend_schemas.awesome.model import AwesomeModel",
        "from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel",
    }
    py_path = model_cls.__module__.replace(".", "/") + ".py"
    if not os.path.exists(py_path):
        py_path = os.path.join(
            "uaproject_backend_schemas", "models.schemas", py_path.split("/")[-1]
        )
    py_imports = parse_imports_from_py(py_path)
    used_types = extract_types_from_fields(model_cls, fields)
    imports = set(base_imports)
    imports |= collect_imports_from_types(used_types, std_types, py_imports, model_cls)
    imports |= collect_imports_from_generated_content(model_cls, std_types)
    return imports


def _get_field_annotation(model_cls: Type[AwesomeModel], field_name: str) -> Any:
    """Gets the type annotation for a field from the model, searching in all relevant places."""
    ann: Any = Any  # Default to Any

    if field_name in model_cls.model_fields:
        ann = model_cls.model_fields[field_name].annotation
    elif (
        hasattr(model_cls, "model_computed_fields")
        and field_name in model_cls.model_computed_fields
    ):
        computed_field = model_cls.model_computed_fields[field_name]
        if hasattr(computed_field, "return_type") and computed_field.return_type:
            ann = computed_field.return_type
    elif field_name in _collect_computed_fields(model_cls):
        computed_field = _collect_computed_fields(model_cls)[field_name]
        if hasattr(computed_field.fget, "__annotations__"):
            ann = computed_field.fget.__annotations__.get("return", Any)
    elif field_name in model_cls.__annotations__:
        ann = model_cls.__annotations__[field_name]

    return ann


def generate_with_permissions_method(class_name: str, all_permissions: set[str]) -> str:
    permissions_literal = " , ".join(f'"{p}"' for p in all_permissions)
    return f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {class_name}: ...\n\n"


def _get_schema_fields(
    model_cls: Type[AwesomeModel], schema_name: str, _type: str = "Schema"
) -> list[str]:
    """Get fields for a specific schema or scope definition."""
    if _type.lower() == "schema":
        home = getattr(model_cls, "Schemas", None)
    else:
        home = getattr(model_cls, "Scopes", None)

    if not home:
        return []

    definition = getattr(home, snake_to_camel(schema_name), None)
    if not definition:
        return []

    all_fields = list(model_cls.model_fields.keys())

    computed_fields = _collect_computed_fields(model_cls)
    all_fields.extend(computed_fields.keys())

    rels = _get_relationship_fields(model_cls)
    all_fields.extend(rels)

    if hasattr(definition, "fields") and definition.fields:
        return definition.fields

    excluded = getattr(definition, "fields_exclude", []) or []
    return [f for f in all_fields if f not in excluded]


def _get_schema_definition(
    model_cls: Type[AwesomeModel], schema_name: str, _type: str = "Schema"
) -> Any:
    """Get schema definition object with all its properties."""
    if _type.lower() == "schema":
        home = getattr(model_cls, "Schemas", None)
    else:
        home = getattr(model_cls, "Scopes", None)

    if not home:
        return None

    return getattr(home, snake_to_camel(schema_name), None)


def generate_class(
    model_cls: Type[AwesomeModel],
    schema_name: str,
    permissions: list[str] = None,
    _type: str = "Schema",
) -> str:
    """Generate schema class with permissions."""
    camel_schema_name = snake_to_camel(schema_name)
    class_name = f"{model_cls.__name__}{_type}{camel_schema_name}"
    if permissions:
        class_name += "WithPermissions"
        class_name += "".join(
            _format_permission_class_name("", p)[len("WithPermissions") :]
            for p in sorted(permissions)
        )

    schema_fields = _get_schema_fields(model_cls, schema_name, _type)
    schema_definition = _get_schema_definition(model_cls, schema_name, _type)

    # Get optional setting from schema definition
    optional_setting = getattr(schema_definition, "optional", None) if schema_definition else None

    fields = []

    for field_name in schema_fields:
        ann = _get_field_annotation(model_cls, field_name)
        field_type_str = _extract_clean_type(ann)

        # Apply optional logic based on schema definition
        if optional_setting is True:
            # All fields are optional
            if not field_type_str.startswith("Optional["):
                field_type_str = f"Optional[{field_type_str}]"
        elif isinstance(optional_setting, list) and field_name in optional_setting:
            # Specific field is optional
            if not field_type_str.startswith("Optional["):
                field_type_str = f"Optional[{field_type_str}]"

        fields.append(f"    {field_name}: {field_type_str}")

    docstring = f'    """{schema_name} schema for {model_cls.__name__} model'
    if permissions:
        docstring += f" with permissions {', '.join(permissions)}"
    docstring += '"""\n'

    fields_str = "\n".join(fields) if fields else "    pass"
    content = f"class {class_name}(AwesomeBaseModel):\n{docstring}\n{fields_str}\n\n"

    all_permissions = get_permissions_from_model(model_cls)
    if all_permissions:
        permissions_literal = " , ".join(f'"{p}"' for p in all_permissions)
        content += f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {class_name}: ...\n\n"
    return content


def _format_permission_class_name(base_name: str, perm: str) -> str:
    """Format permission class name, replacing dots with underscores."""
    return f"{base_name}WithPermissions{''.join(p.capitalize() for p in perm.replace('.', '_').split('_'))}"


def ensure_stub_dir(module_path: str, project_root: Path) -> Path:
    """Create and return stub directory path preserving module structure."""
    parts = module_path.split(".")
    package_root = project_root / parts[0]
    stub_dir = package_root / "/".join(parts[1:-1])
    stub_dir.mkdir(parents=True, exist_ok=True)
    return stub_dir


def generate_filters_class(model_cls: Type[AwesomeModel]) -> str:
    if not hasattr(model_cls, "filters") or not model_cls.filters:
        return ""
    content = f"class {model_cls.__name__}Filters:\n"
    content += f'    """Declarative filters for the {model_cls.__name__} model."""\n'
    for filter_key in model_cls.filters.list():
        filter_cls = getattr(model_cls.Filters, filter_key)
        content += f"    {filter_key}: type\n"
    content += "\n"
    for filter_key in model_cls.filters.list():
        filter_cls = getattr(model_cls.Filters, filter_key)
        content += f"class {model_cls.__name__}Filter{filter_key}(FilterDefinition):\n"
        content += f'    """{getattr(filter_cls, "description", "")}"""\n'
        content += f"    field: str = '{getattr(filter_cls, 'field', '')}'\n"
        if hasattr(filter_cls, "type") and getattr(filter_cls, "type", None):
            content += f"    type: type = {getattr(filter_cls, 'type').__name__}\n"
        content += "\n"
    return content


def generate_sorts_class(model_cls: Type[AwesomeModel]) -> str:
    if not hasattr(model_cls, "sorts") or not model_cls.sorts:
        return ""
    content = f"class {model_cls.__name__}Sorts:\n"
    content += f'    """Declarative sorts for the {model_cls.__name__} model."""\n'
    for sort_key in model_cls.sorts.list():
        sort_cls = getattr(model_cls.Sorts, sort_key)
        content += f"    {sort_key}: type\n"
    content += "\n"
    for sort_key in model_cls.sorts.list():
        sort_cls = getattr(model_cls.Sorts, sort_key)
        content += f"class {model_cls.__name__}Sort{sort_key}(SortDefinition):\n"
        content += f'    """{getattr(sort_cls, "description", "")}"""\n'
        content += f"    field: str = '{getattr(sort_cls, 'field', '')}'\n"
        if hasattr(sort_cls, "direction") and getattr(sort_cls, "direction", None):
            content += f"    direction: str = '{getattr(sort_cls, 'direction', 'asc')}'\n"
        content += "\n"
    return content


def unwrap_optional(ann):
    origin = get_origin(ann)
    if origin is Union:
        args = [a for a in get_args(ann) if a is not type(None)]
        if args:
            return args[0]
        return ann
    return ann


def generate_filter_class(model_cls: Type[AwesomeModel], filter_cls=None) -> str:
    if filter_cls is None:
        if not hasattr(model_cls, "filter") or not model_cls.filter:
            return ""
        filter_cls = model_cls.filter

    content = f"class {model_cls.__name__}Filter(BaseModel):\n"
    content += f'    """Pydantic-class for filtering the {model_cls.__name__} model."""\n'
    for name, field in filter_cls.model_fields.items():
        if name in model_cls.model_fields:
            ann = model_cls.model_fields[name].annotation
            typ = unwrap_optional(ann)
            typ_str = typ.__name__ if hasattr(typ, "__name__") else str(typ)
            content += f"    {name}: Optional[{typ_str}] = None\n"
        else:
            content += f"    {name}: Optional[Any] = None\n"
    content += "\n"
    return content


def generate_sort_enum(model_cls: Type[AwesomeModel], sort_cls=None) -> str:
    if sort_cls is None:
        if not hasattr(model_cls, "sort") or not model_cls.sort:
            return ""
        sort_cls = model_cls.sort

    content = f"class {model_cls.__name__}Sort(StrEnum):\n"
    content += f'    """Enum for sorting the {model_cls.__name__} model."""\n'
    for member in sort_cls:
        content += f"    {member.name} = '{member.value}'\n"
    content += "\n"
    return content


def collect_additional_imports(generated_content: str) -> set[str]:
    imports = set()
    if "BaseModel" in generated_content:
        imports.add("from pydantic import BaseModel")
    if "StrEnum" in generated_content:
        imports.add("from enum import StrEnum")
    if "FilterDefinition" in generated_content:
        imports.add("from uaproject_backend_schemas.awesome.filters import FilterDefinition")
    if "SortDefinition" in generated_content:
        imports.add("from uaproject_backend_schemas.awesome.sorts import SortDefinition")
    if "Any" in generated_content:
        imports.add("from typing import Any")
    # Check for Optional usage in filter/sort classes specifically
    if "Optional[" in generated_content and "from typing import Optional" not in generated_content:
        imports.add("from typing import Optional")
    return imports


def _get_relationship_fields(model_cls: Type[AwesomeModel]) -> list[str]:
    rels = []
    for name in getattr(model_cls, "__annotations__", {}):
        if name not in model_cls.model_fields:
            rels.append(name)
    return rels


def _extract_clean_type(ann: Any) -> str:
    """
    Recursively constructs a type hint string from a type annotation,
    correctly handling generics, optionals, and forward references.
    """
    if isinstance(ann, str):
        return ann

    origin = get_origin(ann)

    # Handle Mapped from SQLAlchemy by unwrapping it and processing the inner type.
    if origin is Mapped:
        args = get_args(ann)
        return _extract_clean_type(args[0]) if args else "Any"

    # Handle ForwardRef objects by extracting their argument as a string
    if hasattr(ann, "__forward_arg__"):
        return ann.__forward_arg__

    args = get_args(ann)

    # Not a generic type (e.g., int, str, a custom class)
    if origin is None:
        return getattr(ann, "__name__", str(ann))

    # Special handling for Optional[T] which is represented as Union[T, None]
    if origin is Union and len(args) == 2 and args[1] is type(None):
        # We only need to represent the T part
        return f"Optional[{_extract_clean_type(args[0])}]"

    # For other generics like List[T], Dict[K, V], etc.
    origin_name = getattr(origin, "_name", None) or getattr(origin, "__name__", "Any")
    if not args:
        return origin_name

    inner_types = ", ".join(_extract_clean_type(arg) for arg in args)
    return f"{origin_name}[{inner_types}]"


def camel_to_snake(name):
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def get_all_subclasses(cls):
    """Recursively get all subclasses of a class."""
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(get_all_subclasses(subclass))
    return subclasses


MODEL_IMPORT_OVERRIDES = {
    "Token": "user_token",
}


def _collect_computed_fields(cls: Type[AwesomeModel]) -> dict[str, Any]:
    fields = {}
    for base in cls.__mro__:
        if not inspect.isclass(base) or not issubclass(base, AwesomeModel):
            continue
        for name, value in inspect.getmembers(base):
            if isinstance(value, property) and getattr(value, "__computed_field__", False):
                fields[name] = value
    return fields


def _generate_model_fields(model_cls: Type[AwesomeModel]) -> str:
    lines = []
    all_field_names = list(model_cls.model_fields.keys())
    all_field_names.extend(_collect_computed_fields(model_cls).keys())
    all_field_names.extend(_get_relationship_fields(model_cls))

    # Use a set to avoid duplicate fields from inheritance
    for field_name in sorted(set(all_field_names)):
        ann = _get_field_annotation(model_cls, field_name)
        field_type = _extract_clean_type(ann)
        lines.append(f"    {field_name}: {field_type}")

    return "\n".join(lines) + "\n"


def _generate_schema_and_scope_sections(
    model_cls: Type[AwesomeModel], permissions: set[str]
) -> str:
    """Generates schema and scope class definitions for the model."""
    content = ""
    for _type in ["schemas", "scopes"]:
        _type_instance = getattr(model_cls, _type, None)

        content += f"class {model_cls.__name__}{_type.capitalize()}:\n"
        content += f'    """{_type.capitalize()} for the {model_cls.__name__} model."""\n'

        if not _type_instance:
            raise ValueError(f"No {_type[:-1]} found for {model_cls.__name__}")

        for _type_key in _type_instance.list():
            base_schema = (
                f"{model_cls.__name__}{_type.capitalize()[:-1]}{snake_to_camel(_type_key)}"
            )
            content += f"    {_type_key}: {base_schema}\n"

        content += "\n"

        for _type_key in _type_instance.list():
            content += generate_class(model_cls, _type_key, _type=_type.capitalize()[:-1])
            for perm in permissions:
                content += generate_class(
                    model_cls, _type_key, [perm], _type=_type.capitalize()[:-1]
                )
    return content


def _reset_cached_properties(model_cls: Type[AwesomeModel]):
    """Resets cached filter and sort attributes to avoid stale data."""
    for prop in ["__filters__", "__sorts__"]:
        try:
            if hasattr(model_cls, prop):
                delattr(model_cls, prop)
        except (AttributeError, TypeError):
            pass


def _generate_filter_section(model_cls: Type[AwesomeModel]) -> str:
    """Generates declarative filters and Pydantic filter class definitions."""
    content = ""
    if (
        hasattr(model_cls, "filters")
        and model_cls.filters
        and hasattr(model_cls.filters, "list")
        and model_cls.filters.list()
    ):
        content += generate_filters_class(model_cls)

    from uaproject_backend_schemas.awesome.filters import AwesomeFilters

    filters_cls = type(f"{model_cls.__name__}Filters", (AwesomeFilters,), {"model_cls": model_cls})
    filter_obj = filters_cls.get_pydantic_filter_class()

    if filter_obj and hasattr(filter_obj, "model_fields") and bool(filter_obj.model_fields):
        content += generate_filter_class(model_cls, filter_obj)
    return content


def _generate_sort_section(model_cls: Type[AwesomeModel]) -> str:
    """Generates declarative sorts and Enum sort class definitions."""
    content = ""
    if (
        hasattr(model_cls, "sorts")
        and model_cls.sorts
        and hasattr(model_cls.sorts, "list")
        and model_cls.sorts.list()
    ):
        content += generate_sorts_class(model_cls)

    from uaproject_backend_schemas.awesome.sorts import AwesomeSorts

    sorts_cls = type(f"{model_cls.__name__}Sorts", (AwesomeSorts,), {"model_cls": model_cls})
    sort_obj = sorts_cls.get_enum_sort_class()

    if sort_obj and hasattr(sort_obj, "__members__") and bool(sort_obj.__members__):
        content += generate_sort_enum(model_cls, sort_obj)
    return content


def _generate_model_sections(model_cls: Type[AwesomeModel], permissions: set[str]) -> str:
    content = _generate_schema_and_scope_sections(model_cls, permissions)

    # Force regeneration of filter/sort to avoid cached classproperty issues
    _reset_cached_properties(model_cls)

    content += _generate_filter_section(model_cls)
    content += _generate_sort_section(model_cls)
    return content


def build_main_content(model_cls: Type[AwesomeModel], permissions: set[str]) -> str:
    main_content = ""
    model_fields_str = _generate_model_fields(model_cls)
    main_content += f"class {model_cls.__name__}(AwesomeModel):\n"
    main_content += f'    """Base {model_cls.__name__.lower()} model."""\n'
    main_content += model_fields_str
    main_content += f"    schemas: {model_cls.__name__}Schemas\n"
    main_content += f"    scopes: {model_cls.__name__}Scopes\n"
    if (
        hasattr(model_cls, "filters")
        and model_cls.filters
        and hasattr(model_cls.filters, "list")
        and model_cls.filters.list()
    ):
        main_content += f"    filters: {model_cls.__name__}Filters\n"
    if (
        hasattr(model_cls, "sorts")
        and model_cls.sorts
        and hasattr(model_cls.sorts, "list")
        and model_cls.sorts.list()
    ):
        main_content += f"    sorts: {model_cls.__name__}Sorts\n"

    # Check for Pydantic filter class - force regeneration to avoid cache issues
    from uaproject_backend_schemas.awesome.filters import AwesomeFilters

    # Create fresh filters instance for this model
    filters_cls = type(f"{model_cls.__name__}Filters", (AwesomeFilters,), {"model_cls": model_cls})
    filter_obj = filters_cls.get_pydantic_filter_class()

    if filter_obj and hasattr(filter_obj, "model_fields") and bool(filter_obj.model_fields):
        main_content += f"    filter: type[{model_cls.__name__}Filter]\n"

    # Check for sort enum - force regeneration to avoid cache issues
    from uaproject_backend_schemas.awesome.sorts import AwesomeSorts

    # Create fresh sorts instance for this model
    sorts_cls = type(f"{model_cls.__name__}Sorts", (AwesomeSorts,), {"model_cls": model_cls})
    sort_obj = sorts_cls.get_enum_sort_class()

    if sort_obj and hasattr(sort_obj, "__members__") and bool(sort_obj.__members__):
        main_content += f"    sort: type[{model_cls.__name__}Sort]\n"
    main_content += "\n"
    main_content += _generate_model_sections(model_cls, permissions)
    return main_content


def generate_stub_for_model(model_cls: Type[AwesomeModel]) -> str:
    """Generate stub content for a single model."""
    return generate_pyi_for_model(model_cls, model_cls.__module__)


def generate_pyi_for_model(model_cls: Type[AwesomeModel], module_path: str) -> str:
    permissions = get_permissions_from_model(model_cls)

    all_field_names = list(model_cls.model_fields.keys())
    all_field_names.extend(_collect_computed_fields(model_cls).keys())
    all_field_names.extend(_get_relationship_fields(model_cls))
    all_field_names = list(set(all_field_names))

    imports = get_required_imports(model_cls, all_field_names)
    std_imports = sorted(
        [
            imp
            for imp in imports
            if imp.startswith("from datetime")
            or imp.startswith("from uuid")
            or imp.startswith("from decimal")
        ]
    )
    typing_imports = sorted([imp for imp in imports if imp.startswith("from typing")])
    project_imports = sorted(
        [imp for imp in imports if imp.startswith("from uaproject_backend_schemas")]
    )
    other_imports = sorted(imports - set(std_imports) - set(typing_imports) - set(project_imports))
    content = (
        PYI_HEADER
        + "\n".join(std_imports + typing_imports + project_imports + other_imports)
        + "\n\n"
    )

    main_content = build_main_content(model_cls, permissions)

    additional_imports = collect_additional_imports(main_content)
    already_imported = set(std_imports + typing_imports + project_imports + other_imports)

    # Parse existing imports to check what's already there
    existing_imports_text = "\n".join(
        std_imports + typing_imports + project_imports + other_imports
    )

    additional_imports = [
        imp
        for imp in additional_imports
        if imp not in already_imported and imp not in existing_imports_text
    ]
    if additional_imports:
        content += "\n".join(additional_imports) + "\n\n"

    content += main_content
    return content


def _discover_models() -> tuple[dict[str, Type[AwesomeModel]], defaultdict[str, list]]:
    """Discover unique models from module paths."""
    unique_models = {}
    model_to_modules = defaultdict(list)

    for module_path in MODEL_MODULES:
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"Failed to import {module_path}: {e}")
            continue

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, AwesomeModel) and obj != AwesomeModel:
                if name not in unique_models:
                    unique_models[name] = obj
                model_to_modules[name].append(module_path)

    print(f"📊 Found {len(unique_models)} unique models across {len(MODEL_MODULES)} modules")
    return unique_models, model_to_modules


def _generate_stubs(
    unique_models: dict, model_to_modules: defaultdict, project_root: Path
) -> list[Path]:
    """Generate .pyi stub files for each unique model."""
    generated_files = []
    for name, obj in unique_models.items():
        module_path = model_to_modules[name][0]
        stub_dir = ensure_stub_dir(module_path, project_root)
        stub_file = stub_dir / f"{camel_to_snake(name)}.pyi"

        file_start_time = time.perf_counter()
        print(f"📝 Generating .pyi for {obj.__name__} -> {camel_to_snake(name)}.pyi")

        pyi_content = generate_pyi_for_model(obj, module_path)

        with open(stub_file, "w") as f:
            f.write(pyi_content)

        file_end_time = time.perf_counter()
        file_duration = file_end_time - file_start_time
        print(f"   ✅ Generated in {file_duration:.3f}s")

        generated_files.append(stub_file)
    return generated_files


def _format_stubs_individually(generated_files: list[Path]):
    """Fallback to format stub files individually."""
    print("🔄 Falling back to individual file processing...")
    for stub_file in generated_files:
        try:
            subprocess.run(["ruff", "format", str(stub_file)], check=True)
            subprocess.run(["ruff", "check", "--fix", str(stub_file)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to process {stub_file}: {e}")


def _format_stubs(generated_files: list[Path]):
    """Format generated stub files using ruff."""
    if not generated_files:
        return

    print(f"⚡ Batch formatting {len(generated_files)} files with ruff...")
    try:
        format_cmd = ["ruff", "format"] + [str(f) for f in generated_files]
        subprocess.run(format_cmd, check=True, capture_output=True, text=True)
        print(f"✅ Formatted {len(generated_files)} files")

        fix_cmd = ["ruff", "check", "--fix"] + [str(f) for f in generated_files]
        subprocess.run(fix_cmd, check=True, capture_output=True, text=True)
        print(f"✅ Fixed imports in {len(generated_files)} files")

    except subprocess.CalledProcessError as e:
        print(f"❌ Batch ruff processing failed: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        _format_stubs_individually(generated_files)
    except FileNotFoundError:
        print("❌ ruff not found. Please install ruff to enable formatting.")


def main():
    """Stub generation with deduplication and batch processing."""

    print("🚀 Starting stub generation...")
    start_time = time.perf_counter()

    project_root = Path(__file__).parent.parent.parent

    unique_models, model_to_modules = _discover_models()
    generated_files = _generate_stubs(unique_models, model_to_modules, project_root)
    _format_stubs(generated_files)

    end_time = time.perf_counter()
    duration = end_time - start_time

    if not generated_files:
        print("✅ No models found to generate stubs for.")
        return

    print(f"🎉 Generated {len(generated_files)} stub files in {duration:.3f} seconds")
    print(f"📈 Average: {duration / len(generated_files):.3f}s per file")


if __name__ == "__main__":
    main()
