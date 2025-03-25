from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, HttpUrl

__all__ = ["SortOrder", "DefaultSort", "UserDefaultSort", "RedirectUrlResponse", "SerializableHttpUrl", "SerializableDecimal"]


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
    def __str__(self):
        return str(self)

    @classmethod
    def parse_obj(cls, value: Any) -> "SerializableHttpUrl":
        if isinstance(value, str):
            return cls(value)
        return super().parse_obj(value)


class SerializableDecimal(Decimal):
    def __str__(self):
        return str(self)

    @classmethod
    def parse_obj(cls, value: Any) -> "SerializableDecimal":
        if isinstance(value, str):
            return cls(value)
        return super().parse_obj(value)
