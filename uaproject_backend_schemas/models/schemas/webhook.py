from enum import StrEnum


class WebhookStatus(StrEnum):
    ACTIVE = "active"
    UNRESPONSIVE = "unresponsive"
    PROCESSING = "processing"
    ERROR = "error"
