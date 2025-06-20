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

from uaproject_backend_schemas.awesome.fields import AwesomeFieldInfo
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
        if hasattr(field, "required_permissions"):
            permissions.update(field.required_permissions)

    permissions.update(_get_schema_permissions(model_cls))

    return permissions


def _check_field_needs(field_info: Any, needs: dict) -> str:
    """Check field needs and update the needs dict."""
    field_type = str(field_info.annotation)
    needs["optional"] |= "Optional" in field_type
    needs["list"] |= "List" in field_type
    needs["dict"] |= "Dict" in field_type
    needs["datetime"] |= "datetime" in field_type
    needs["awesome_field"] |= hasattr(field_info, "required_permissions")
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
    for field in fields:
        if field not in model_cls.model_fields:
            continue
        ann = model_cls.model_fields[field].annotation
        extract_types_recursively(ann, used_types)
    for name, value in inspect.getmembers(model_cls):
        if isinstance(value, property) and getattr(value, "__computed_field__", False):
            tp = value.fget.__annotations__.get("return", None)
            if tp:
                extract_types_recursively(tp, used_types)
    return used_types


def collect_imports_from_types(used_types, std_types, py_imports, model_cls) -> set:
    imports = set()
    already_imported = set()
    for tp in used_types:
        if tp in std_types:
            imports.add(std_types[tp])
            already_imported.add(tp)
        elif tp in py_imports and tp not in already_imported:
            imports.add(py_imports[tp])
            already_imported.add(tp)

    for name, obj in inspect.getmembers(importlib.import_module(model_cls.__module__)):
        if inspect.isclass(obj) and name in used_types and name not in already_imported:
            if hasattr(obj, "__bases__") and any("Enum" in str(base) for base in obj.__bases__):
                model_name = model_cls.__name__.lower()
                schema_module_path = f"uaproject_backend_schemas.models.schemas.{model_name}"
                try:
                    schema_module = importlib.import_module(schema_module_path)
                    if hasattr(schema_module, name):
                        imports.add(f"from {schema_module_path} import {name}")
                        already_imported.add(name)
                        continue
                except ImportError:
                    pass

            imports.add(f"from {model_cls.__module__} import {name}")
            already_imported.add(name)
    return imports


def collect_imports_from_generated_content(model_cls, std_types) -> set:
    imports = set()
    all_content = []
    for _type in [("Schema", "schemas"), ("Scope", "scopes")]:
        for schema_key in (
            getattr(model_cls, _type[1], []).list()
            if hasattr(getattr(model_cls, _type[1], None), "list")
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


def _get_field_type(field: Any) -> str:
    """Get field type."""
    field_type = field.annotation.__name__ if hasattr(field, "annotation") else str(field.type_)
    if field_type == "Optional":
        field_type = f"Optional[{field.annotation.__args__[0].__name__}]"
    elif field_type == "List":
        field_type = f"List[{field.annotation.__args__[0].__name__}]"
    return field_type


def _get_field_str(field_name: str, field: Any, field_type: str) -> str:
    """Get string representation of a field."""
    field_str = f"    {field_name}: {field_type}"
    if isinstance(field, AwesomeFieldInfo):
        if field.required_permissions:
            field_str += f" = AwesomeField(required_permissions={field.required_permissions})"
    return field_str


def _should_include_field(field: Any, permissions: list[str] = None) -> bool:
    """Check if a field should be included considering permissions."""
    if not permissions:
        return True
    if hasattr(field, "required_permissions") and all(
        p not in permissions for p in field.required_permissions
    ):
        return False
    return True


def generate_fields(model_cls: Type[AwesomeModel], permissions: list[str] = None) -> list[str]:
    fields = []
    for field_name, field in model_cls.model_fields.items():
        if not _should_include_field(field, permissions):
            continue
        field_type = _get_field_type(field)
        field_str = _get_field_str(field_name, field, field_type)
        fields.append(field_str)
    for name, value in inspect.getmembers(model_cls):
        if isinstance(value, property) and getattr(value, "__computed_field__", False):
            field_type = value.fget.__annotations__.get("return", Any)
            fields.append(f"    {name}: {field_type.__name__}")
    relationships = getattr(model_cls, "__relationships__", [])
    for rel in relationships:
        fields.append(f"    {rel}: Optional[Any] = None")
    return fields


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
    fields = []

    for field_name in schema_fields:
        if field_name in model_cls.model_fields:
            field_type = _get_field_type(model_cls.model_fields[field_name])
            fields.append(f"    {field_name}: {field_type}")
        elif (
            hasattr(model_cls, "model_computed_fields")
            and field_name in model_cls.model_computed_fields
        ):
            computed_field = model_cls.model_computed_fields[field_name]
            if hasattr(computed_field, "return_type") and computed_field.return_type:
                type_str = _extract_clean_type(computed_field.return_type)
            else:
                type_str = "Any"
            fields.append(f"    {field_name}: {type_str}")
        elif field_name in _collect_computed_fields(model_cls):
            computed_field = _collect_computed_fields(model_cls)[field_name]
            if hasattr(computed_field.fget, "__annotations__"):
                return_type = computed_field.fget.__annotations__.get("return", "Any")
                type_str = (
                    return_type.__name__ if hasattr(return_type, "__name__") else str(return_type)
                )
            else:
                type_str = "Any"
            fields.append(f"    {field_name}: {type_str}")
        elif field_name in model_cls.__annotations__:
            ann = model_cls.__annotations__[field_name]
            type_str = _extract_clean_type(ann)
            fields.append(f"    {field_name}: {type_str}")
        else:
            fields.append(f"    {field_name}: Any")

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


def _extract_clean_type(ann):
    ann_str = str(ann)

    # Handle datetime class representation
    if ann_str == "<class 'datetime.datetime'>":
        return "datetime"

    if ann_str.startswith("sqlalchemy.orm.base.Mapped"):
        inner = ann_str.split("[", 1)[1].rsplit("]", 1)[0]
        inner = inner.replace("typing.", "")
        inner = re.sub(r'ForwardRef\(["\\\']?([A-Za-z_][A-Za-z0-9_]*)["\\\']?\)', r"\1", inner)
        inner = re.sub(
            r"uaproject_backend_schemas\.models\.[\w\.]+\.([A-Z][A-Za-z0-9_]*)", r"\1", inner
        )
        if not inner.startswith("Optional["):
            inner = f"Optional[{inner}]"
        return inner

    # Handle computed fields return types without wrapping in Optional
    ann_str = ann_str.replace("typing.", "")
    ann_str = re.sub(r'ForwardRef\(["\\\']?([A-Za-z_][A-Za-z0-9_]*)["\\\']?\)', r"\1", ann_str)
    ann_str = re.sub(
        r"uaproject_backend_schemas\.models\.[\w\.]+\.([A-Z][A-Za-z0-9_]*)", r"\1", ann_str
    )

    # Don't automatically wrap computed field types in Optional
    # Only wrap relationship fields in Optional
    return ann_str


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


def _generate_model_fields(model_cls: Type[AwesomeModel]) -> tuple[str, set]:
    lines = []
    imports = set()
    model_imports = set()

    for field_name, field in model_cls.model_fields.items():
        field_type = _get_field_type(field)
        lines.append(f"    {field_name}: {field_type}")

    if hasattr(model_cls, "model_computed_fields"):
        for field_name, computed_field in model_cls.model_computed_fields.items():
            if hasattr(computed_field, "return_type") and computed_field.return_type:
                type_str = _extract_clean_type(computed_field.return_type)
            else:
                type_str = "Any"
            lines.append(f"    {field_name}: {type_str}")

            # Add imports for computed field types
            if "Optional" in type_str:
                imports.add("from typing import Optional")
            if "List" in type_str:
                imports.add("from typing import List")
            if "Dict" in type_str:
                imports.add("from typing import Dict")
    else:
        computed_fields = _collect_computed_fields(model_cls)
        for field_name, computed_field in computed_fields.items():
            if hasattr(computed_field.fget, "__annotations__"):
                return_type = computed_field.fget.__annotations__.get("return", "Any")
                if hasattr(return_type, "__name__"):
                    type_str = return_type.__name__
                else:
                    type_str = str(return_type)
                lines.append(f"    {field_name}: {type_str}")
            else:
                lines.append(f"    {field_name}: Any")

    rels = _get_relationship_fields(model_cls)
    for rel in rels:
        ann = model_cls.__annotations__[rel]
        type_str = _extract_clean_type(ann)
        if "Optional" in type_str:
            imports.add("from typing import Optional")
        if "List" in type_str:
            imports.add("from typing import List")
        if "Dict" in type_str:
            imports.add("from typing import Dict")
        for match in re.findall(r"\b([A-Z][A-Za-z0-9_]*)\b", type_str):
            if match not in {"Optional", "List", "Dict", "Any", "str", "int", "bool", "float"}:
                filename = MODEL_IMPORT_OVERRIDES.get(match, camel_to_snake(match))
                model_imports.add(
                    f"from uaproject_backend_schemas.models.{filename} import {match}"
                )
        lines.append(f"    {rel}: {type_str}")

    all_imports = imports | model_imports
    return "\n".join(lines) + "\n", all_imports


def _generate_model_sections(model_cls: Type[AwesomeModel], permissions: set[str]) -> str:
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

    # Generate declarative filters and filter classes only if they exist and have content
    if (
        hasattr(model_cls, "filters")
        and model_cls.filters
        and hasattr(model_cls.filters, "list")
        and model_cls.filters.list()
    ):
        content += generate_filters_class(model_cls)

    # Force regeneration of filter/sort to avoid cached classproperty issues
    # Reset cached filter/sort attributes if they exist
    try:
        if hasattr(model_cls, "__filters__"):
            delattr(model_cls, "__filters__")
    except (AttributeError, TypeError):
        pass
    try:
        if hasattr(model_cls, "__sorts__"):
            delattr(model_cls, "__sorts__")
    except (AttributeError, TypeError):
        pass

    # Check for Pydantic filter class - force regeneration to avoid cache issues
    from uaproject_backend_schemas.awesome.filters import AwesomeFilters

    # Create fresh filters instance for this model
    filters_cls = type(f"{model_cls.__name__}Filters", (AwesomeFilters,), {"model_cls": model_cls})
    filter_obj = filters_cls.get_pydantic_filter_class()

    if filter_obj and hasattr(filter_obj, "model_fields") and bool(filter_obj.model_fields):
        content += generate_filter_class(model_cls, filter_obj)

    # Generate sorts classes only if they exist and have content
    if (
        hasattr(model_cls, "sorts")
        and model_cls.sorts
        and hasattr(model_cls.sorts, "list")
        and model_cls.sorts.list()
    ):
        content += generate_sorts_class(model_cls)

    # Check for sort enum - force regeneration to avoid cache issues
    from uaproject_backend_schemas.awesome.sorts import AwesomeSorts

    # Create fresh sorts instance for this model
    sorts_cls = type(f"{model_cls.__name__}Sorts", (AwesomeSorts,), {"model_cls": model_cls})
    sort_obj = sorts_cls.get_enum_sort_class()

    if sort_obj and hasattr(sort_obj, "__members__") and bool(sort_obj.__members__):
        content += generate_sort_enum(model_cls, sort_obj)
    return content


def build_main_content(model_cls: Type[AwesomeModel], permissions: set[str]) -> str:
    main_content = ""
    model_fields_str, all_imports = _generate_model_fields(model_cls)
    if all_imports:
        main_content += "\n".join(sorted(all_imports)) + "\n\n"
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
    all_fields = list(model_cls.model_fields.keys())

    imports = get_required_imports(model_cls, all_fields)
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
    existing_imports_text = "\n".join(std_imports + typing_imports + project_imports + other_imports)
    
    additional_imports = [imp for imp in additional_imports if imp not in already_imported and imp not in existing_imports_text]
    if additional_imports:
        content += "\n".join(additional_imports) + "\n\n"

    content += main_content
    return content


def main():
    """Optimized stub generation with deduplication and batch processing."""

    print("🚀 Starting optimized stub generation...")
    start_time = time.perf_counter()

    project_root = Path(__file__).parent.parent.parent

    unique_models = {}
    model_to_modules = defaultdict(list)

    for module_path in MODEL_MODULES:
        module = importlib.import_module(module_path)

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, AwesomeModel) and obj != AwesomeModel:
                if name not in unique_models:
                    unique_models[name] = obj
                model_to_modules[name].append(module_path)

    print(f"📊 Found {len(unique_models)} unique models across {len(MODEL_MODULES)} modules")

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

    print(f"⚡ Batch formatting {len(generated_files)} files with ruff...")
    try:
        format_cmd = ["ruff", "format"] + [str(f) for f in generated_files]
        subprocess.run(format_cmd, check=True)
        print(f"✅ Formatted {len(generated_files)} files")

        fix_cmd = ["ruff", "check", "--fix"] + [str(f) for f in generated_files]
        subprocess.run(fix_cmd, check=True)
        print(f"✅ Fixed imports in {len(generated_files)} files")

    except subprocess.CalledProcessError as e:
        print(f"❌ Batch ruff processing failed: {e}")
        print("🔄 Falling back to individual file processing...")
        for stub_file in generated_files:
            try:
                subprocess.run(["ruff", "format", str(stub_file)], check=True)
                subprocess.run(["ruff", "check", "--fix", str(stub_file)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to process {stub_file}: {e}")
    except FileNotFoundError:
        print("❌ ruff not found. Please install ruff to enable formatting.")

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"🎉 Generated {len(generated_files)} stub files in {duration:.3f} seconds")
    print(f"📈 Average: {duration / len(generated_files):.3f}s per file")


if __name__ == "__main__":
    main()
