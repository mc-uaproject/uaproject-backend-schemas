from enum import StrEnum

from pydantic import BaseModel

__all__ = ["SortOrder", "DefaultSort", "UserDefaultSort"]


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
