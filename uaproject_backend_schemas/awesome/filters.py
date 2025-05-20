from datetime import date, datetime
from typing import Any, List, Optional, Type, TypeVar, get_args, get_origin

from pydantic import BaseModel, create_model

TModel = TypeVar("TModel")


class FilterDefinition:
    """
    Base class for declarative description of a filter.
    """

    field: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Any] = None

    def __init__(
        self,
        field: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[Any] = None,
    ):
        if field is not None:
            self.field = field
        if description is not None:
            self.description = description
        if type is not None:
            self.type = type


class AwesomeFilters:
    """
    Manager of filters for the model. Allows to get all available filters.
    """

    exclude: List[str] = []  # Можна перевизначити у нащадку

    def __init__(self, model_cls: Type[TModel]):
        self.model_cls: Type[TModel] = model_cls

    def __repr__(self):
        cls_name = self.__class__.__name__
        model_name = getattr(self.model_cls, "__name__", str(self.model_cls))
        filters = self.list()
        return f"<{cls_name} for {model_name}, filters={filters}>"

    @classmethod
    def list(cls) -> List[str]:
        return [
            name
            for name in dir(cls)
            if not name.startswith("_")
            and isinstance(getattr(cls, name), type)
            and issubclass(getattr(cls, name), FilterDefinition)
        ]

    @classmethod
    def get(cls, name: str) -> Type[FilterDefinition]:
        if hasattr(cls, name):
            return getattr(cls, name)
        raise AttributeError(f"Filter '{name}' not found in {cls.__name__}")

    @classmethod
    def _get_model_cls(cls):
        model_cls = getattr(cls, "model_cls", None)
        if model_cls is None:
            for base in getattr(cls, "__orig_bases__", []):
                if hasattr(base, "__args__") and base.__args__:
                    model_cls = base.__args__[0]
                    break
        if model_cls is None:
            raise RuntimeError("Cannot determine model for filter")
        return model_cls

    @classmethod
    def _build_fields_from_model_fields(cls, model_cls, exclude):
        fields = {}
        for name, field in getattr(model_cls, "model_fields", {}).items():
            if name in exclude:
                continue
            typ = field.annotation
            if get_origin(typ) is Optional:
                typ = get_args(typ)[0]
            fields[name] = (Optional[typ], None)
            if typ in (int, float, datetime, date):
                fields[f"min_{name}"] = (Optional[typ], None)
                fields[f"max_{name}"] = (Optional[typ], None)
        return fields

    @classmethod
    def _build_fields_from_mro(cls, model_cls, exclude, fields):
        for mixin in model_cls.__mro__:
            for mixin_field, typ in getattr(mixin, "__annotations__", {}).items():
                if mixin_field in fields or mixin_field in exclude:
                    continue
                fields[mixin_field] = (Optional[typ], None)
                if typ in (int, float, datetime, date):
                    fields[f"min_{mixin_field}"] = (Optional[typ], None)
                    fields[f"max_{mixin_field}"] = (Optional[typ], None)
        return fields

    @classmethod
    def _build_fields_from_relations(cls, model_cls, exclude, fields):
        for name, attr in model_cls.__dict__.items():
            if hasattr(attr, "property") and hasattr(attr.property, "direction"):
                rel_model = attr.property.mapper.class_
                for rel_field in getattr(rel_model, "model_fields", {}):
                    if rel_field in ("name", "id"):
                        rel_filter_name = f"{name}_{rel_field}"
                        if rel_filter_name not in exclude:
                            fields[rel_filter_name] = (Optional[Any], None)
        return fields

    @classmethod
    def _add_custom_filters(cls, exclude, fields):
        for filter_name in cls.list():
            filter_cls: Type[FilterDefinition] = getattr(cls, filter_name)
            if filter_cls.field and filter_cls.field not in exclude:
                typ: Any = getattr(filter_cls, "type", None) or Optional[Any]
                fields[filter_cls.field] = (typ, None)
        return fields

    @classmethod
    def get_pydantic_filter_class(cls) -> Type[BaseModel]:
        exclude = set(getattr(cls, "exclude", []) or [])
        model_cls = cls._get_model_cls()
        fields = cls._build_fields_from_model_fields(model_cls, exclude)
        fields = cls._build_fields_from_mro(model_cls, exclude, fields)
        fields = cls._build_fields_from_relations(model_cls, exclude, fields)
        fields = cls._add_custom_filters(exclude, fields)
        model: Type[BaseModel] = create_model(f"{model_cls.__name__}AutoFilter", **fields)
        return model
