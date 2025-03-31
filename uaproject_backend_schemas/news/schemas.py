from enum import StrEnum

from pydantic import BaseModel


class NewsType(StrEnum):
    UPDATE = "update"
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OTHER = "other"
    PERSONAL = "personal"
    CONGRATULATION = "congratulation"


class ImportanceType(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class NewsBase(BaseModel):
    title: str
    content: str
    type: NewsType
    importance: ImportanceType
