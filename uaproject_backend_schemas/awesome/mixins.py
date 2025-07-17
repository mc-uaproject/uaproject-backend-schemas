from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, computed_field
from sqlalchemy import BigInteger

from uaproject_backend_schemas.awesome.fields import AwesomeField
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
    model_config = {"serialize_computed_fields": True}

    updated_at: datetime = AwesomeField(
        default_factory=utcnow, sa_column_kwargs={"onupdate": utcnow}, nullable=False
    )

    @computed_field(return_type=datetime)
    @property
    def created_at(self) -> datetime:
        try:
            timestamp_ms = (self.id >> 17) & 0x1FFFFFFFFFF
            result = EPOCH + timedelta(milliseconds=timestamp_ms)
            return result if 1970 <= result.year <= 9999 else EPOCH
        except (OverflowError, ValueError):
            return EPOCH
