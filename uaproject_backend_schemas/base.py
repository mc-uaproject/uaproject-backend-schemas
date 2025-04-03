from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

PayloadBoth = Literal["before", "after"]


class Base(SQLModel): ...


def utcnow():
    return datetime.now(UTC)


class IDMixin(BaseModel):
    id: int | None = Field(default=None, primary_key=True)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class UsersIDMixin(IDMixin):
    user_id: int


class TimestampsMixin(SQLModel):
    created_at: datetime = Field(default_factory=utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=utcnow, sa_column_kwargs={"onupdate": utcnow}, nullable=False
    )


class PayloadBaseModel(BaseModel):
    action: str
    scope: str
    payload: dict[str, Any]


class BothPayloadBaseModel(BaseModel):
    payload: dict[Literal["before", "after"], dict[str, Any]]


PayloadModels = PayloadBaseModel | BothPayloadBaseModel
