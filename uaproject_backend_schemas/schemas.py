from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, HttpUrl
from pydantic_core import core_schema

__all__ = ["SortOrder", "DefaultSort", "UserDefaultSort", "RedirectUrlResponse"]


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


class SerializableHttpUrl(HttpUrl):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(cls),
                    core_schema.no_info_plain_validator_function(
                        lambda value: super().__new__(cls, str(value))
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance), return_schema=core_schema.str_schema()
            ),
        )


class SerializableDecimal(Decimal):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(cls),
                    core_schema.no_info_plain_validator_function(
                        lambda value: super().__new__(cls, str(value))
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance), return_schema=core_schema.str_schema()
            ),
        )

    def __repr__(self):
        return f"SerializableDecimal('{self}')"
