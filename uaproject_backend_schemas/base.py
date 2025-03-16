from datetime import UTC, datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class Base(SQLModel): ...


def utcnow():
    return datetime.now(UTC)


class IDMixin(BaseModel):
    id: int | None = Field(default=None, primary_key=True)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class TimestampsMixin:
    created_at = Column(DateTime, default=utcnow, nullable=True)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=True)
