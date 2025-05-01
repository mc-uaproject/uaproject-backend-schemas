import importlib
import inspect
import os
from typing import Any, Type

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeFieldInfo

MODEL_MODULES = [
    "uaproject_backend_schemas.models.test",
]

PYI_HEADER = """# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
from typing import Literal, Optional

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel, AwesomeField

"""


def get_permissions_from_model(model_cls: Type[AwesomeModel]) -> set[str]:
    """Get all unique permissions from model fields."""
    permissions = set()
    for field in model_cls.model_fields.values():
        if hasattr(field, "exclude_permissions"):
            permissions.update(field.exclude_permissions)
        if hasattr(field, "include_permissions"):
            permissions.update(field.include_permissions)
    return permissions


def _get_field_type(field: Any) -> str:
    """Get field type."""
    field_type = field.annotation.__name__ if hasattr(field, "annotation") else str(field.type_)
    if field_type == "Optional":
        field_type = f"Optional[{field.annotation.__args__[0].__name__}]"
    return field_type


def _get_field_str(field_name: str, field: Any, field_type: str) -> str:
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


def generate_schema_class(
    model_cls: Type[AwesomeModel], schema_name: str, permissions: list[str] = None
) -> str:
    """Generate schema class with permissions."""
    class_name = f"{model_cls.__name__}Schema{schema_name.capitalize()}"
    if permissions:
        class_name += "WithPermissions"
        class_name += "".join(p.capitalize() for p in sorted(permissions))

    fields = []
    for field_name, field in model_cls.model_fields.items():
        if not _should_include_field(field, permissions):
            continue

        field_type = _get_field_type(field)
        field_str = _get_field_str(field_name, field, field_type)
        fields.append(field_str)

    docstring = f'    """{schema_name} schema for {model_cls.__name__} model'
    if permissions:
        docstring += f" with permissions {', '.join(permissions)}"
    docstring += '"""\n'

    content = f"class {class_name}(AwesomeBaseModel):\n{docstring}" + "\n".join(fields) + "\n\n"

    all_permissions = get_permissions_from_model(model_cls)
    if all_permissions:
        if not permissions:
            content += f"class {model_cls.__name__}Schema{schema_name.capitalize()}WithPermissions(AwesomeBaseModel):\n"
            content += (
                f'    """{schema_name} schema for {model_cls.__name__} model with permissions"""\n'
            )
            content += "\n".join(fields) + "\n\n"

        permission_models = [
            f"{model_cls.__name__}Schema{schema_name.capitalize()}WithPermissions{''.join(p.capitalize() for p in sorted([perm]))}"
            for perm in all_permissions
        ]
        permission_models.append(
            f"{model_cls.__name__}Schema{schema_name.capitalize()}WithPermissions"
        )
        return_type = (
            " | ".join(permission_models) if len(permission_models) > 1 else permission_models[0]
        )

        permissions_literal = " | ".join(f'"{p}"' for p in all_permissions)
        content += f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {return_type}: ...\n\n"

    return content


def generate_scope_class(model_cls: Type[AwesomeModel], scope_name: str) -> str:
    """Generate visibility scope class."""
    class_name = f"{model_cls.__name__}Scope{scope_name.capitalize()}"
    fields = model_cls.scopes.resolve_fields(model_cls, scope_name)

    field_strs = []
    for field in fields:
        field_info = model_cls.model_fields[field]
        field_type = _get_field_type(field_info)
        field_strs.append(f"    {field}: {field_type}")

    docstring = f'    """{scope_name} visibility scope for {model_cls.__name__} model"""\n'

    content = f"class {class_name}(AwesomeBaseModel):\n{docstring}" + "\n".join(field_strs) + "\n\n"

    all_permissions = get_permissions_from_model(model_cls)
    if all_permissions:
        content += f"class {model_cls.__name__}Scope{scope_name.capitalize()}WithPermissions(AwesomeBaseModel):\n"
        content += f'    """{scope_name} visibility scope for {model_cls.__name__} model with permissions"""\n'
        content += "\n".join(field_strs) + "\n\n"

        for perm in all_permissions:
            perm_class_name = f"{model_cls.__name__}Scope{scope_name.capitalize()}WithPermissions{perm.capitalize()}"
            perm_fields = []
            for field in fields:
                field_info = model_cls.model_fields[field]
                if not _should_include_field(field_info, [perm]):
                    continue
                field_type = _get_field_type(field_info)
                perm_fields.append(f"    {field}: {field_type}")

            content += f"class {perm_class_name}(AwesomeBaseModel):\n"
            content += f'    """{scope_name} visibility scope for {model_cls.__name__} model with permissions {perm}"""\n'
            content += "\n".join(perm_fields) + "\n\n"

        permission_models = [
            f"{model_cls.__name__}Scope{scope_name.capitalize()}WithPermissions{''.join(p.capitalize() for p in sorted([perm]))}"
            for perm in all_permissions
        ]
        permission_models.append(
            f"{model_cls.__name__}Scope{scope_name.capitalize()}WithPermissions"
        )
        return_type = (
            " | ".join(permission_models) if len(permission_models) > 1 else permission_models[0]
        )

        permissions_literal = " | ".join(f'"{p}"' for p in all_permissions)
        content += f"    def with_permissions(self, permissions: list[Literal[{permissions_literal}]]) -> {return_type}: ...\n\n"

    return content


def generate_pyi_for_model(model_cls: Type[AwesomeModel]) -> str:
    """Generate .pyi file content for a model (description of its schemas)."""
    permissions = get_permissions_from_model(model_cls)

    content = f"class {model_cls.__name__}(AwesomeModel):\n"
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
        content += f"    {scope_key}: {model_cls.__name__}Scope{scope_key.capitalize()}\n"

    content += "\n"

    for schema_key in model_cls.schemas.list():
        content += generate_schema_class(model_cls, schema_key)
        for perm in permissions:
            content += generate_schema_class(model_cls, schema_key, [perm])

    for scope_key in model_cls.scopes.list():
        content += generate_scope_class(model_cls, scope_key)

    return content


def main():
    for module_path in MODEL_MODULES:
        module = importlib.import_module(module_path)

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, AwesomeModel) and obj != AwesomeModel:
                file_path = os.path.abspath(module.__file__)
                pyi_path = file_path.replace(".py", ".pyi")

                print(f"Generating .pyi for {obj.__name__} at {pyi_path}")

                pyi_content = PYI_HEADER + generate_pyi_for_model(obj)

                with open(pyi_path, "w") as f:
                    f.write(pyi_content)


if __name__ == "__main__":
    main()
