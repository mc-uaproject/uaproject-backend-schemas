from decimal import Decimal
from enum import StrEnum
from typing import Any, TypeVar
from urllib.parse import urlparse

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from sqlalchemy.orm import DeclarativeBase

__all__ = [
    "SortOrder",
    "DefaultSort",
    "UserDefaultSort",
    "RedirectUrlResponse",
    "SerializableHttpUrl",
    "SerializableDecimal",
    "ModelType",
    "CreateSchemaType",
    "UpdateSchemaType",
    "FilterSchemaType",
]


ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class DefaultSort(StrEnum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class UserDefaultSort(StrEnum):
    ID = DefaultSort.ID
    CREATED_AT = DefaultSort.CREATED_AT
    UPDATED_AT = DefaultSort.UPDATED_AT
    USER_ID = "user_id"


class RedirectUrlResponse(BaseModel):
    url: str


class SerializableHttpUrl(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        def validate(value: Any) -> str:
            if isinstance(value, str):
                # Validate URL
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


class SerializableDecimal(Decimal):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: Any) -> Decimal:
            if isinstance(value, str):
                try:
                    return Decimal(value)
                except Exception:
                    raise ValueError("Invalid Decimal value")
            elif isinstance(value, (int, float, Decimal, cls)):
                return Decimal(value)
            raise ValueError("Invalid Decimal type")

        def serialize(value: Any) -> str:
            return str(value)

        schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.str_schema(),
                core_schema.float_schema(),
                core_schema.int_schema(),
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
