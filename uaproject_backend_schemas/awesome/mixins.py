from datetime import UTC, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, computed_field
from sqlalchemy import BigInteger

from uaproject_backend_schemas.awesome.utils import AwesomeField
from uaproject_backend_schemas.utils.id_generator import UAIdGenerator

id_generator = UAIdGenerator()
EPOCH = id_generator.epoch


def utcnow() -> datetime:
    return datetime.now(UTC)


class IDMixin(BaseModel):
    id: int = AwesomeField(
        default_factory=id_generator.generate, sa_type=BigInteger, primary_key=True
    )

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class TimestampsMixin(BaseModel):
    updated_at: datetime = AwesomeField(
        default_factory=utcnow, sa_column_kwargs={"onupdate": utcnow}, nullable=False
    )

    @computed_field
    @property
    def created_at(self) -> Optional[datetime]:
        try:
            seconds = self.id // 1_000_000
            result = EPOCH + timedelta(milliseconds=seconds)
            return result if 1970 <= result.year <= 9999 else None
        except (OverflowError, ValueError):
            return None
