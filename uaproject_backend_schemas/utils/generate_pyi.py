import ast
import importlib
import inspect
import os
from datetime import datetime
from pathlib import Path
from typing import Any, List, Type

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeFieldInfo


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
    MODEL_MODULES.extend(expand_wildcard_modules(module))

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
        if hasattr(field, "exclude_permissions"):
            permissions.update(field.exclude_permissions)
        if hasattr(field, "include_permissions"):
            permissions.update(field.include_permissions)

    permissions.update(_get_schema_permissions(model_cls))

    return permissions


def _check_field_needs(field_info: Any, needs: dict) -> str:
    """Check field needs and update the needs dict."""
    field_type = str(field_info.annotation)
    needs["optional"] |= "Optional" in field_type
    needs["list"] |= "List" in field_type
    needs["dict"] |= "Dict" in field_type
    needs["datetime"] |= "datetime" in field_type
    needs["awesome_field"] |= hasattr(field_info, "exclude_permissions") or hasattr(
        field_info, "include_permissions"
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
            imports.add(f"from {model_cls.__module__} import {name}")
            already_imported.add(name)
    return imports


def collect_imports_from_generated_content(model_cls, std_types) -> set:
    imports = set()
    all_content = []
    for schema_key in (
        getattr(model_cls, "schemas", []).list()
        if hasattr(getattr(model_cls, "schemas", None), "list")
        else []
    ):
        all_content.append(generate_schema_class(model_cls, schema_key))
    for scope_key in (
        getattr(model_cls, "scopes", []).list()
        if hasattr(getattr(model_cls, "scopes", None), "list")
        else []
    ):
        all_content.append(generate_scope_class(model_cls, scope_key))
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
        "AwesomeField": "from uaproject_backend_schemas.awesome.utils import AwesomeField",
    }
    base_imports = {
        "from uaproject_backend_schemas.awesome.model import AwesomeModel",
        "from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel",
    }
    py_path = model_cls.__module__.replace(".", "/") + ".py"
    if not os.path.exists(py_path):
        py_path = os.path.join("uaproject_backend_schemas", "models", py_path.split("/")[-1])
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


def _get_field_str(
    field_name: str, field: Any, field_type: str, include_relationships: bool = False
) -> str:
    """Get string representation of a field."""
    field_str = f"    {field_name}: {field_type}"
    if isinstance(field, AwesomeFieldInfo):
        if field.exclude_permissions:
            field_str += f" = AwesomeField(exclude_permissions={field.exclude_permissions})"
        elif field.include_permissions:
            field_str += f" = AwesomeField(include_permissions={field.include_permissions})"
    return field_str


def _should_include_field(field: Any, permissions: list[str] = None) -> bool:
    """Check if a field should be included considering permissions."""
    if not permissions:
        return True
    if hasattr(field, "exclude_permissions") and any(
        p in permissions for p in field.exclude_permissions
    ):
        return False
    if hasattr(field, "include_permissions") and not any(
        p in permissions for p in field.include_permissions
    ):
        return False
    return True


def generate_schema_fields(model_cls: Type[AwesomeModel], permissions: list[str] = None) -> list[str]:
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
    permission_models = [
        _format_permission_class_name(class_name, perm)
        for perm in all_permissions
    ]
    permission_models.append(f"{class_name}WithPermissions")
    return_type = (
        " | ".join(permission_models)
        if len(permission_models) > 1 else permission_models[0]
    )
    permissions_literal = " , ".join(f'"{p}"' for p in all_permissions)
    return f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {return_type}: ...\n\n"


def generate_with_permissions_class(model_cls: Type[AwesomeModel], schema_name: str, fields: list[str]) -> str:
    class_name = f"{model_cls.__name__}Schema{schema_name.capitalize()}WithPermissions"
    docstring = f'    """{schema_name} schema for {model_cls.__name__} model with permissions"""\n'
    return f"class {class_name}(AwesomeBaseModel):\n" + docstring + "\n".join(fields) + "\n\n"


def generate_schema_class(
    model_cls: Type[AwesomeModel], schema_name: str, permissions: list[str] = None
) -> str:
    """Generate schema class with permissions."""
    class_name = f"{model_cls.__name__}Schema{schema_name.capitalize()}"
    if permissions:
        class_name += "WithPermissions"
        class_name += "".join(
            _format_permission_class_name("", p)[len("WithPermissions") :]
            for p in sorted(permissions)
        )

    fields = generate_schema_fields(model_cls, permissions)
    docstring = f'    """{schema_name} schema for {model_cls.__name__} model'
    if permissions:
        docstring += f" with permissions {', '.join(permissions)}"
    docstring += '"""\n'
    content = f"class {class_name}(AwesomeBaseModel):\n{docstring}" + "\n".join(fields) + "\n\n"

    all_permissions = get_permissions_from_model(model_cls)
    if all_permissions:
        if not permissions:
            content += generate_with_permissions_method(f"{model_cls.__name__}Schema{schema_name.capitalize()}", all_permissions)
            content += generate_with_permissions_class(model_cls, schema_name, fields)
        permission_models = [
            _format_permission_class_name(
                f"{model_cls.__name__}Schema{schema_name.capitalize()}", perm
            )
            for perm in all_permissions
        ]
        permission_models.append(
            f"{model_cls.__name__}Schema{schema_name.capitalize()}WithPermissions"
        )
        return_type = (
            " | ".join(permission_models)
            if len(permission_models) > 1 else permission_models[0]
        )
        permissions_literal = " , ".join(f'"{p}"' for p in all_permissions)
        content += f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {return_type}: ...\n\n"
    return content


def _get_field_str_for_scope(model_cls: Type[AwesomeModel], field: str) -> str:
    """Get field string representation for scope."""
    if hasattr(model_cls, field):
        field_value = getattr(model_cls, field)
        if isinstance(field_value, property) and getattr(field_value, "__computed_field__", False):
            field_type = field_value.fget.__annotations__.get("return", Any)
            return f"    {field}: {field_type.__name__}"

    if field in model_cls.model_fields:
        field_info = model_cls.model_fields[field]
        field_type = _get_field_type(field_info)
        return f"    {field}: {field_type}"
    return ""


def _get_scope_fields(
    model_cls: Type[AwesomeModel], fields: List[str], perm: str = None
) -> List[str]:
    """Get field strings for scope."""
    field_strs = []
    for field in fields:
        field_str = _get_field_str_for_scope(model_cls, field)
        if not field_str:
            continue
        if perm and field in model_cls.model_fields:
            field_info = model_cls.model_fields[field]
            if not _should_include_field(field_info, [perm]):
                continue
        field_strs.append(field_str)
    return field_strs


def _format_permission_class_name(base_name: str, perm: str) -> str:
    """Format permission class name, replacing dots with underscores."""
    return f"{base_name}WithPermissions{''.join(p.capitalize() for p in perm.replace('.', '_').split('_'))}"


def generate_scope_class(model_cls: Type[AwesomeModel], scope_name: str) -> str:
    """Generate visibility scope class."""
    scope_name_camel = "".join(word.capitalize() for word in scope_name.split("_"))
    class_name = f"{model_cls.__name__}Scope{scope_name_camel}"
    fields = model_cls.scopes.resolve_fields(model_cls, scope_name)

    field_strs = _get_scope_fields(model_cls, fields)

    for rel in getattr(model_cls, "__relationships__", []):
        field_strs.append(f"    {rel}: Optional[Any] = None")

    content = [
        f"class {class_name}(AwesomeBaseModel):",
        f'    """{scope_name} visibility scope for {model_cls.__name__} model"""',
        *field_strs,
        "",
    ]

    all_permissions = get_permissions_from_model(model_cls)
    if all_permissions:
        base_perm_class = f"{model_cls.__name__}Scope{scope_name_camel}WithPermissions"
        content.extend(
            [
                f"class {base_perm_class}(AwesomeBaseModel):",
                f'    """{scope_name} visibility scope for {model_cls.__name__} model with permissions"""',
                *field_strs,
                "",
            ]
        )

        for perm in all_permissions:
            perm_class = _format_permission_class_name(
                f"{model_cls.__name__}Scope{scope_name_camel}", perm
            )
            perm_fields = _get_scope_fields(model_cls, fields, perm)
            content.extend(
                [
                    f"class {perm_class}(AwesomeBaseModel):",
                    f'    """{scope_name} visibility scope for {model_cls.__name__} model with permissions {perm}"""',
                    *perm_fields,
                    "",
                ]
            )

        permission_models = [
            _format_permission_class_name(f"{model_cls.__name__}Scope{scope_name_camel}", p)
            for p in all_permissions
        ]
        permission_models.append(base_perm_class)
        return_type = (
            " | ".join(permission_models) if len(permission_models) > 1 else permission_models[0]
        )
        permissions_literal = ", ".join(f'"{p}"' for p in all_permissions)
        content.append(
            f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {return_type}: ..."
        )

    return "\n".join(content) + "\n\n"


def ensure_stub_dir(module_path: str, project_root: Path) -> Path:
    """Create and return stub directory path preserving module structure."""
    parts = module_path.split(".")
    package_root = project_root / parts[0]
    stub_dir = package_root / "/".join(parts[1:-1])
    stub_dir.mkdir(parents=True, exist_ok=True)
    return stub_dir


def generate_pyi_for_model(model_cls: Type[AwesomeModel], module_path: str) -> str:
    """Generate .pyi file content for a model (description of its schemas)."""
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
    content = "# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.\n\n"
    content += "\n".join(std_imports + typing_imports + project_imports + other_imports) + "\n\n"

    content += f"class {model_cls.__name__}(AwesomeModel):\n"
    content += '    """Base user model."""\n'
    content += f"    schemas: {model_cls.__name__}Schemas\n"
    content += f"    scopes: {model_cls.__name__}Scopes\n\n"

    content += f"class {model_cls.__name__}Schemas:\n"
    content += '    """Schemas for the user model."""\n'
    for schema_key in model_cls.schemas.list():
        base_schema = f"{model_cls.__name__}Schema{schema_key.capitalize()}"
        content += f"    {schema_key}: {base_schema}\n"

    content += "\n"

    content += f"class {model_cls.__name__}Scopes:\n"
    content += '    """Visibility scopes for the user model."""\n'
    for scope_key in model_cls.scopes.list():
        scope_name_parts = scope_key.split("_")
        scope_name_camel = "".join(word.capitalize() for word in scope_name_parts)
        content += f"    {scope_key}: {model_cls.__name__}Scope{scope_name_camel}\n"

    content += "\n"

    for schema_key in model_cls.schemas.list():
        content += generate_schema_class(model_cls, schema_key)
        for perm in permissions:
            content += generate_schema_class(model_cls, schema_key, [perm])

    for scope_key in model_cls.scopes.list():
        content += generate_scope_class(model_cls, scope_key)

    return content


def main():
    project_root = Path(__file__).parent.parent.parent

    for module_path in MODEL_MODULES:
        module = importlib.import_module(module_path)
        stub_dir = ensure_stub_dir(module_path, project_root)

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, AwesomeModel) and obj != AwesomeModel:
                stub_file = stub_dir / f"{module_path.split('.')[-1]}.pyi"

                print(f"Generating .pyi for {obj.__name__} at {stub_file}")

                pyi_content = generate_pyi_for_model(obj, module_path)

                with open(stub_file, "w") as f:
                    f.write(pyi_content)

                try:
                    import subprocess

                    subprocess.run(["ruff", "format", str(stub_file)], check=True)
                    print(f"Formatted {stub_file} with ruff")

                    subprocess.run(["ruff", "check", "--fix", str(stub_file)], check=True)
                    print(f"Fixed imports in {stub_file} with ruff")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to process {stub_file}: {e}")
                except FileNotFoundError:
                    print("ruff not found. Please install ruff to enable formatting.")


if __name__ == "__main__":
    main()
