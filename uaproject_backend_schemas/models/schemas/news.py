from enum import StrEnum


class NewsType(StrEnum):
    UPDATE = "update"
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OTHER = "other"
    PERSONAL = "personal"
    CONGRATULATION = "congratulation"
    TECHNICAL = "technical"
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    QUEST = "quest"
    RECRUITMENT = "recruitment"
    HOLIDAY = "holiday"


class ImportanceType(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"
    EMERGENCY = "emergency"
