from typing import Any
from urllib.parse import urlparse

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


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
