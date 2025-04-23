from uaproject_backend_schemas.users.schemas import UserResponse

from .schemas import (
    CreateSchemaType,
    DefaultSort,
    FilterSchemaType,
    ModelType,
    RedirectUrlResponse,
    SerializableDecimal,
    SerializableHttpUrl,
    SortOrder,
    UpdateSchemaType,
    UserDefaultSort,
)

__all__ = [
    "DefaultSort",
    "SortOrder",
    "UserDefaultSort",
    "RedirectUrlResponse",
    "SerializableHttpUrl",
    "SerializableDecimal",
    "ModelType",
    "CreateSchemaType",
    "UpdateSchemaType",
    "FilterSchemaType",
]

def initialize_models():
    UserResponse.initialize()
