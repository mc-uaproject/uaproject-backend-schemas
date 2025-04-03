from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
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


class TimestampsMixin(BaseModel):
    created_at = Column(DateTime, default=utcnow, nullable=True)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=True)


class PayloadBaseModel(BaseModel):
    action: str
    scope: str
    payload: dict[str, Any]


class BothPayloadBaseModel(BaseModel):
    payload: dict[Literal["before", "after"], dict[str, Any]]


PayloadModels = PayloadBaseModel | BothPayloadBaseModel
