from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, computed_field, model_serializer
from sqlmodel import BigInteger, Field, SQLModel

from uaproject_backend_schemas.id_generator import UAIdGenerator

PayloadBoth = Literal["before", "after"]

id_generator = UAIdGenerator()
EPOCH = id_generator.epoch


class Base(SQLModel): ...


def utcnow():
    return datetime.now(UTC)


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, int) and abs(value) > 2**53:
                result[key] = str(value)
            else:
                result[key] = value
        return result


class IDMixin(BaseModel):
    id: int = Field(default_factory=id_generator.generate, sa_type=BigInteger, primary_key=True)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class UsersIDMixin(IDMixin):
    user_id: int


class TimestampsMixin(BaseModel):
    updated_at: datetime = Field(
        default_factory=utcnow, sa_column_kwargs={"onupdate": utcnow}, nullable=False
    )

    computed_field(return_type=Optional[datetime])

    @property
    def created_at(self) -> Optional[datetime]:
        try:
            seconds = self.id // 1_000_000
            result = EPOCH + timedelta(milliseconds=seconds)
            return result if 1970 <= result.year <= 9999 else None
        except (OverflowError, ValueError):
            return None


class PayloadBaseModel(BaseModel):
    action: str
    scope: str
    payload: dict[str, Any]


class BothPayloadBaseModel(BaseModel):
    payload: dict[Literal["before", "after"], dict[str, Any]]


PayloadModels = PayloadBaseModel | BothPayloadBaseModel
